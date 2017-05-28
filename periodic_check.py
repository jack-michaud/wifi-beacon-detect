import checks

if __name__ == "__main__":
    print "Running all main functions in the modules in checks:"

    for key in checks.__dict__:
        if '__' not in key:
            checks.__dict__[key].main()

    
