#!/usr/bin/env python

from __future__ import print_function

import sys
try:
    import configparser
    from future import standard_library
    import builtins
except ImportError:
    sys.stderr.write("Updates to cosmosis mean that you now need to install some new packages.\n")
    sys.stderr.write("Please install with: pip install configparser future\n")
    sys.stderr.write("On some environments these might need to be installed separately - sorry\n")
    sys.exit(1)

standard_library.install_aliases()
from builtins import zip
import argparse
import os
import pdb
from .runtime.config import Inifile, CosmosisConfigurationError
from .runtime.pipeline import LikelihoodPipeline
from .runtime import mpi_pool
from .runtime import process_pool
from .runtime.utils import ParseExtraParameters, stdout_redirected
from .samplers.sampler import Sampler, ParallelSampler, Hints
from . import output as output_module


RUNTIME_INI_SECTION = "runtime"


def experimental_fault_handling():
    import  cosmosis.runtime.handler
    cosmosis.runtime.handler.activate_experimental_fault_handling()


def demo_1_special (args):
    if "demo1.ini" in args.inifile:
        print()
        print("Congratulations: you have just run cosmosis demo one!")
        if os.path.exists("./conda"):
            print() 
            print("You can make plots of the outputs of this using this command:")
            print("  postprocess demos/demo1.ini -o plots -p demo1")
            print()
            print("If you get a message about 'Abort Trap 6' then see the FAQ:")
            print("https://bitbucket.org/joezuntz/cosmosis/wiki/FAQ")
            print()
            print("Then you can try out the other demos...")
            print("... and read the information about plotting their output and what they are doing online.")
            print("Please get in touch with any problems, ideally by filing an Issue. Thanks!")
        else:
            print("You can make plots of the outputs of this using the command:")
            print()
            print("postprocess demos/demo1.ini -o plots -p demo1")
            print()
            print("Then you can try out the other demos...")
            print("... and read the information about plotting their output and what they are doing online.")
            print("Please get in touch with any problems, ideally by filing an Issue. Thanks!")
            print()


def demo_10_special (args):
    if   "demo10.ini" in args.inifile   and   not os.getenv ("HALOFIT", ""):
        print()
        print("Welcome to demo10!")
        print()
        print("**PLEASE NOTE**:")
        print()
        print("There are two flavours of this demo, selected through an ")
        print("environment variable called `HALOFIT'; this variable is not ")
        print("currently set, so we are giving it the value `halofit'.")
        print("Please see the wiki for more information: ")
        print("https://bitbucket.org/joezuntz/cosmosis/wiki/Demo10.")

        os.environ ["HALOFIT"] = "halofit"



def demo_20a_special (args):
    if  "demo20a.ini" in args.inifile:
        print ()
        print ("You have completed demo20a, now run demo20b and compare")
        print ("results with demo5!")


def demo_20b_special (args):
    if   "demo20b.ini" in args.inifile   and   not os.path.isfile ("./demo20a.txt"):
        print ()
        print ("********************************************************")
        print ("*** YOU MUST RUN demo20a BEFORE YOU CAN RUN demo20b. ***")
        print ("********************************************************")

def sampler_main_loop(sampler, output, pool):
    # Run the sampler until convergence
    # which really means "finished" here - 
    # a sampler can "converge" just by reaching the 
    # limit of the number of samples it is allowed.
    if not pool or pool.is_master():
        while not sampler.is_converged():
            sampler.execute()
            #Flush any output. This is to stop
            #a problem in some MPI cases where loads
            #of output is built up before being written.
            if output:
                output.flush()
        # If we are in parallel tell the other processors to end the 
        # loop and prepare for the next sampler
        if pool and sampler.is_parallel_sampler:
            pool.close()
    else:
        if sampler.is_parallel_sampler:
            sampler.worker()



def write_header_output(output, params, values, pipeline):
    # If there is an output file, save the ini information to
    # it as well.  We do it here since it's nicer to have it
    # after the sampler options that get written in sampler.config.
    # Create a buffer to store the output:
    output.comment("START_OF_PARAMS_INI")
    comment_wrapper = output.comment_file_wrapper()
    params.write(comment_wrapper)
    output.comment("END_OF_PARAMS_INI")
    # Do the same with the values file.
    # Unfortunately that means reading it in again;
    # if we ever refactor this bit we could eliminate that.
    if values is None:
        values_ini=Inifile(pipeline.values_filename)
    else:
        values_ini=values
    output.comment("START_OF_VALUES_INI")
    values_ini.write(comment_wrapper)
    output.comment("END_OF_VALUES_INI")

    # And the same with the priors
    output.comment("START_OF_PRIORS_INI")
    for priors_file in pipeline.priors_files:
        prior_ini=Inifile(priors_file)
        prior_ini.write(comment_wrapper)
    output.comment("END_OF_PRIORS_INI")

def setup_output(sampler_class, sampler_number, ini, pool, number_samplers, sample_method):

    needs_output = sampler_class.needs_output and \
       (pool is None or pool.is_master() or sampler_class.parallel_output)

    if not needs_output:
        return None


    #create the output files and methods.
    try:
        output_options = dict(ini.items('output'))
    except configparser.NoSectionError:
        raise ValueError("ERROR:\nFor the sampler (%s) you chose in the [runtime] section of the ini file I also need an [output] section describing how to save results\n\n"%sample_method)
    #Additionally we tell the output here if
    #we are parallel or not.
    if (pool is not None) and (sampler_class.parallel_output):
        output_options['rank'] = pool.rank
        output_options['parallel'] = pool.size

    #Give different output filenames to the different sampling steps
    #Only change if this is not the last sampling step - the final
    #one retains the name in the output file.
    # Change, e.g. demo17.txt to demo17.fisher.txt
    if ("filename" in output_options) and (sampler_number<number_samplers-1):
        filename = output_options['filename']
        filename, ext = os.path.splitext(filename)
        filename += '.' + sampler_name
        filename += ext
        output_options['filename'] = filename


    #Generate the output from a factory
    output = output_module.output_from_options(output_options)
    output.metadata("sampler", sample_method)

    if ("filename" in output_options):
        print("* Saving output -> {}".format(output_options['filename']))

    return output


def run_cosmosis(args, pool=None, ini=None, pipeline=None, values=None):
    # In case we need to hand-hold a naive demo-10 user.

    # Load configuration.
    if ini is None:
        ini = Inifile(args.inifile, override=args.params)

    pre_script = ini.get(RUNTIME_INI_SECTION, "pre_script", fallback="")
    post_script = ini.get(RUNTIME_INI_SECTION, "post_script", fallback="")

    if (pool is None) or pool.is_master():
        # This decodes the exist status
        status = os.WEXITSTATUS(os.system(pre_script))
        if status:
            raise RuntimeError("The pre-run script {} retuned non-zero status {}".format(
                pre_script, status))

    # Create pipeline.
    if pipeline is None:
        cleanup_pipeline = True
        pool_stdout = ini.getboolean(RUNTIME_INI_SECTION, "pool_stdout", fallback=False)
        if (pool is None) or pool.is_master() or pool_stdout:
            pipeline = LikelihoodPipeline(ini, override=args.variables, values=values, only=args.only)
        else:
            # Suppress output on everything except the master process
            if pool_stdout:
                pipeline = LikelihoodPipeline(ini, override=args.variables, only=args.only) 
            else:
                with stdout_redirected():
                    pipeline = LikelihoodPipeline(ini, override=args.variables, only=args.only) 

        if pipeline.do_fast_slow:
            pipeline.setup_fast_subspaces()
    else:
        # We should not cleanup a pipeline which we didn't make
        cleanup_pipeline = False




    # determine the type(s) of sampling we want.
    sample_methods = ini.get(RUNTIME_INI_SECTION, "sampler", fallback="test").split()

    for sample_method in sample_methods:
        if sample_method not in Sampler.registry:
            raise ValueError("Unknown sampler method %s" % (sample_method,))

    #Get that sampler from the system.
    sampler_classes = [Sampler.registry[sample_method] for sample_method in sample_methods]

    if pool:
        if not any(issubclass(sampler_class,ParallelSampler) for sampler_class in sampler_classes):
            if len(sampler_classes)>1:
                raise ValueError("None of the samplers you chose support parallel execution!")
            else:
                raise ValueError("The sampler you chose does not support parallel execution!")
        for sampler_class in sampler_classes:
            if isinstance(pool, process_pool.Pool) and issubclass(sampler_class,ParallelSampler) and not sampler_class.supports_smp:
                name = sampler_class.__name__[:-len("Sampler")].lower()
                raise ValueError("Sorry, the {} sampler does not support the --smp flag.".format(name))

    number_samplers = len(sampler_classes)


    #To start with we do not have any estimates of 
    #anything the samplers might give us like centers
    #or covariances. 
    distribution_hints = Hints()

    #Now that we have a sampler we know whether we will need an
    #output file or not.  By default new samplers do need one.
    for sampler_number, (sampler_class, sample_method) in enumerate(
            zip(sampler_classes, sample_methods)):
        sampler_name = sampler_class.__name__[:-len("Sampler")].lower()

        # The resume feature lets us restart from an existing file.
        # It's not fully rolled out to all the suitable samplers yet though.
        resume = ini.getboolean(RUNTIME_INI_SECTION, "resume", fallback=False)

        # Not all samplers can be resumed.
        if resume and not sampler_class.supports_resume:
            print("NOTE: You set resume=T in the [runtime] section but the sampler {} does not support resuming yet.  I will ignore this option.".format(sampler_name))
            resume=False

        if pool is None or pool.is_master():
            print("****************************")
            print("* Running sampler {}/{}: {}".format(sampler_number+1,number_samplers, sampler_name))

        output = setup_output(sampler_class, sampler_number, ini, pool, number_samplers, sample_method)
        print("****************************")

        #Initialize our sampler, with the class we got above.
        #It needs an extra pool argument if it is a ParallelSampler.
        #All the parallel samplers can also act serially too.
        if pool and sampler_class.is_parallel_sampler:
            sampler = sampler_class(ini, pipeline, output, pool)
        else:
            sampler = sampler_class(ini, pipeline, output)
         
        #Set up the sampler - for example loading
        #any resources it needs or checking the ini file
        #for additional parameters.
        sampler.distribution_hints.update(distribution_hints)
        sampler.config()

        # Potentially resume
        if resume and sampler_class.needs_output and \
            sampler_class.supports_resume and \
           (pool is None 
            or pool.is_master() 
            or sampler_class.parallel_output):
           sampler.resume()

        if output:
            write_header_output(output, ini, values, pipeline)

        sampler_main_loop(sampler, output, pool)

        distribution_hints.update(sampler.distribution_hints)

        if output:
            output.close()

    if cleanup_pipeline:
        pipeline.cleanup()


    # User can specify in the runtime section a post-run script to launch.
    # In general this may be less useful than the pre-run script, because
    # often chains time-out instead of actually completing.
    # But we still offer it
    if (pool is None) or pool.is_master():
        # This decodes the exist status
        status = os.WEXITSTATUS(os.system(post_script))
        if status:
            sys.stdout.write("WARNING: The post-run script {} failed with error {}".format(
                post_script, error))

    return 0


def main():
    try:
        parser = argparse.ArgumentParser(description="Run a pipeline with a single set of parameters", add_help=True)
        parser.add_argument("inifile", help="Input ini file of parameters")
        parser.add_argument("--mpi",action='store_true',help="Run in MPI mode.")
        parser.add_argument("--smp",type=int,default=0,help="Run with the given number of processes in shared memory multiprocessing (this is experimental and does not work for multinest).")
        parser.add_argument("--pdb",action='store_true',help="Start the python debugger on an uncaught error. Only in serial mode.")
        parser.add_argument("--experimental-fault-handling",action='store_true',help="Activate an experimental fault handling mode.")
        parser.add_argument("-p", "--params", nargs="*", action=ParseExtraParameters, help="Override parameters in inifile, with format section.name1=value1 section.name2=value2...")
        parser.add_argument("-v", "--variables", nargs="*", action=ParseExtraParameters, help="Override variables in values file, with format section.name1=value1 section.name2=value2...")
        parser.add_argument("--only", nargs="*", help="Fix all parameters except the ones listed")
        args = parser.parse_args(sys.argv[1:])


        demo_10_special (args)
        demo_20b_special (args)

        if args.experimental_fault_handling:
            experimental_fault_handling()

        # initialize parallel workers
        if args.mpi:
            with mpi_pool.MPIPool() as pool:
                return run_cosmosis(args,pool)
        elif args.smp:
            with process_pool.Pool(args.smp) as pool:
                return run_cosmosis(args,pool)
        else:
            try:
                return run_cosmosis(args)
            except Exception as error:
                if args.pdb:
                    print("There was an exception - starting python debugger because you ran with --pdb")
                    print(error)
                    pdb.post_mortem()
                else:
                    raise
    except CosmosisConfigurationError as e:
        print(e)
        return 1

    # Extra-special actions we take to mollycoddle a brand-new user!
    demo_1_special (args)
    demo_20a_special (args)


if __name__=="__main__":
    status = main()
    sys.exit(status)
