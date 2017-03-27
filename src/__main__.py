import os, sys, inspect

def main(args=None):

    ##Finding project dir

    cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
    cmd_folder = cmd_folder[0:cmd_folder.find("src")]
    sys.path.append(cmd_folder)
    sys.path.append(cmd_folder+"src/")

    import descriptive_statistics
    import kgrams_CAH
    import dbscan_kmeans
    import step_customer_journey
    import influet_events

    # Do argument parsing here (eg. with argparse) and anything else
    # you want your project to do.

if __name__ == "__main__":
    main()
