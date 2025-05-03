import sys
import config

# Get the output option, dataset option(s), & tile size from the user
def welcome_user():
    print('\nWelcome to Ctrl+Tile: Photographic Mosaic Generator!')
    retry = 0

    # Get the output option
    print('\nChoose your mosaic output by typing S or W:')
    print('  S: still image (make sure to place your (1) desired image in the Input_Image folder)')
    print('  W: webcam frame (make sure your webcam is available for use)')
    outputOption = input().strip().upper()
    
    if outputOption not in ['S', 'W']:
        retry = 1

        while (retry == 1):
            print('  Invalid output option. Try again. You can also quit the program by typing Q')
            outputOption = input().strip().upper()

            if outputOption == 'Q':
                sys.exit()
            elif outputOption in ['S', 'W']:
                retry = 0
                break

    # Get the dataset option(s)
    print('\nChoose your dataset(s) by typing one or more of the following:')
    print('  U: user uploaded (make sure to place your images in the User_Uploaded folder)')
    print('  P: portraits (500 images of people & animals)')
    print('  A: abstract (500 images of art, patterns, & colors)')
    print('  L: landscapes (500 images of nature)')
    print('  M: materials (500 images of buildings, objects, & food)')
    print('For example: type "UPALM" to use all datasets')
    datasetOption = input().strip().upper()

    for opt in datasetOption:
        if opt not in ['U', 'P', 'A', 'L', 'M']:
            retry = 1
            break

    while (retry == 1):
        anotherRetry = 0

        print('  Contains an invalid dataset option. Try again. You can also quit the program by typing Q')
        datasetOption = input().strip().upper()

        if datasetOption == 'Q':
            sys.exit()

        for opt in datasetOption:
            if opt not in ['U', 'P', 'A', 'L', 'M']:
                anotherRetry = 1
                break

        if anotherRetry == 1:
            continue

        retry = 0

    # exclude webcam users from tile size option
    if outputOption == 'W':
        tileSize = (10, 10)
        Tiled_Images = config.x10Path
    
    #handle still image logic. Return placed inside of the if statement to avoid "tileOption" return error
    else:
        print('\nChoose your tile size by typing one of the following:')
        print('  1: 5x5 (smallest tiles)')
        print('  2: 10x10')
        print('  3: 15x15')
        print('  4: 20x20 (largest tiles)')
        tileOption = input().strip()

        if tileOption not in ['1', '2', '3', '4']:
            retry = 1

            while (retry == 1):
                print('  Invalid tile size option. Try again. You can also quit the program by typing Q')
                tileOption = input().strip()

                if tileOption in ['Q', 'q']:
                    sys.exit()
                elif tileOption in ['1', '2', '3', '4']:
                    retry = 0
                    break

        if tileOption == '1':
            tileSize = (5, 5)
            Tiled_Images = config.x5Path
        elif tileOption == '2':
            tileSize = (10, 10)
            Tiled_Images = config.x10Path
        elif tileOption == '3':
            tileSize = (15, 15)
            Tiled_Images = config.x15Path
        elif tileOption == '4':
            tileSize = (20, 20)
            Tiled_Images = config.x20Path

        # Update config
        config.datasetOption = datasetOption
        config.tileSize = tileSize
        config.Tiled_Images = Tiled_Images
        config.outputOption = outputOption

    return outputOption, datasetOption, tileSize, Tiled_Images
