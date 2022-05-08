#A group of functions to measure errors on image denoising

#One can measure the error made when denoising an image one of two ways: count the total amount pixels that are wrong by comparison with the real picture
#or count the pixels that truly impact the quallity of the image.

#The first method is implemented under the totalError(picture1, picture2) function
#The second method is implemented under the qualityError(picture1, picture2, neighbourThreshold) function


#Required packages: numpy


import numpy as np

def findErrors(picture1, picture2):
    '''A function that finds all non-equal pixels in a picture
    @param picture1, picture2: the picture that are compared
    @return an array with the indices of the errors'''
    
    assert picture1.size == picture2.size, 'Both pictures must be the same size'
    data1 = np.asarray(picture1)
    data2 = np.asarray(picture2)
    return(np.where(data1 != data2))


def totalError(picture1, picture2):
    ''' A function that computes the total differences between two pictures, i.e the amount of different pixels.
    @param picture1, picture2: the pictures that are being compared
    @return the total amount of errors in the work picture'''
    
    return(len(findErrors(picture1, picture2)[0]))

def neighboursOfSameColour(pixel:int, neighboursColours:list):
    '''A method that counts how many neighbouring pixels are of the same colour as a chosen pixel
    @param pixel: of type int, represents the colour of the pixel that is checked
    @param neighboursColours: a list containing the colours of the neighbours
    @return the amount of neigbours with the same colour as the test pixel '''
    total = 0
    for i in range (0,len(neighboursColours)):
        if neighboursColours[i] == pixel:
            total += 1
    return(total)

def qualityError(picture1, picture2, neighbourThreshold):
    '''A function that computes the quality error of a certain picture compared to the original. It takes a wrong pixel,
    and checks if the pixel has any neighbours of the same "wrong" colour. If enough neighbours are of the same colour
    (enough being defined by neighbourThreshold), it concludes that this pixel is not a quality error, and the error is not
    counted
    @param workPicture: the picture worked with
    @param realPicture: the real picture the working picture is compared to
    @return the amount of quality errors in the work picture'''
    
    assert picture1.size == picture2.size, 'Both pictures must have the same size'
    
    qualityErrors = 0 #the counter for all the quality errors we will encounter
    
    errors = findErrors(picture1, picture2) #les indices de toutes les erreurs
    totalErrors = len(errors[0])
    
    workData = np.asarray(picture1)
    
    width = workData.shape[0]
    height = workData.shape[1]
    
    for i in range(totalErrors):
        wrong_x, wrong_y = errors[0][i], errors[1][i] # on prend les coordonnées des pixels faux
        wrongColour = workData[wrong_x][wrong_y]
        #on doit comparer les pixels faux à leurs voisins, mais il faut faire attention à la localisation de ces pixels
        #si les pixels sont sur les bors, ils ont moins de voisins
        if wrong_x == 0: #pixel tout à gauche de l'image
            if wrong_y == 0: #pixel tout en haut à gauche, 3 voisins
                neighbours = [workData[wrong_x][wrong_y + 1], workData[wrong_x + 1][wrong_y], workData[wrong_x +1][wrong_y+1]]
                if neighboursOfSameColour(wrongColour, neighbours) < neighbourThreshold:
                    qualityErrors += 1
            elif wrong_y == height -1 : #pixel tout en bas à gauche, 3 voisins
                neighbours = [workData[wrong_x][wrong_y-1], workData[wrong_x + 1][wrong_y], workData[wrong_x+1][wrong_y -1]]
                if neighboursOfSameColour(wrongColour, neighbours) < neighbourThreshold:
                    qualityErrors += 1
            else: #pixel tout à gauche, mais pas sur un coin, 5 voisins
                neighbours = [workData[wrong_x][wrong_y-1], workData[wrong_x][wrong_y+1], workData[wrong_x + 1][wrong_y -1],
                             workData[wrong_x+1][wrong_y], workData[wrong_x+1][wrong_y +1]]
                if neighboursOfSameColour(wrongColour, neighbours) < neighbourThreshold:
                    qualityErrors += 1
        elif wrong_x == width -1: #pixel tout à droit de l'image
            if wrong_y == 0: #pixel tout en haut à droite, 3 voisins
                neighbours = [workData[wrong_x][wrong_y +1], workData[wrong_x-1][wrong_y], workData[wrong_x-1][wrong_y+1]]
                if neighboursOfSameColour(wrongColour, neighbours) < neighbourThreshold:
                    qualityErrors += 1
            elif wrong_y == height -1: #pixel tout en bas à droite, 3 voisins
                neighbours = [workData[wrong_x][wrong_y -1], workData[wrong_x -1][wrong_y], workData[wrong_x][wrong_y -1]]
                if neighboursOfSameColour(wrongColour, neighbours) < neighbourThreshold:
                    qualityErrors += 1
            else: #pixel tout à droite, mais pas sur un coin, 5 voisins
                neighbours = [workData[wrong_x][wrong_y - 1], workData[wrong_x][wrong_y + 1], workData[wrong_x - 1][wrong_y-1],
                             workData[wrong_x-1][wrong_y], workData[wrong_x -1][wrong_y + 1]]
                if neighboursOfSameColour(wrongColour, neighbours) < neighbourThreshold:
                    qualityErrors += 1
        else: #pixel ni sur un bord gauche ou droit de l'image
            #reste à traiter le cas des pixels en haut ou en bas, puis au centre de l'image
            if wrong_y == 0: #pixel en haut, mais pas sur un coin (cas déjà traité), 5 voisins
                neighbours = [workData[wrong_x-1][wrong_y], workData[wrong_x +1 ][wrong_y], workData[wrong_x-1][wrong_y+1],
                             workData[wrong_x][wrong_y+1], workData[wrong_x+1][wrong_y +1]]
                if neighboursOfSameColour(wrongColour, neighbours) < neighbourThreshold:
                    qualityErrors += 1
            elif wrong_y == height -1 : #pixel en bas, mais pas sur un coin (déjà traité), 5 voisins
                neighbours = [workData[wrong_x-1][wrong_y], workData[wrong_x +1][wrong_y], workData[wrong_x-1][wrong_y -1],
                             workData[wrong_x][wrong_y -1 ], workData[wrong_x+1][wrong_y-1]]
                if neighboursOfSameColour(wrongColour, neighbours) < neighbourThreshold:
                    qualityErrors += 1
            else: #pixel sur aucun bord de l'image, 8 voisins
                neighbours = [workData[wrong_x -1][wrong_y -1], workData[wrong_x -1][wrong_y], workData[wrong_x][wrong_y +1],
                             workData[wrong_x][wrong_y - 1], workData[wrong_x][wrong_y + 1], workData[wrong_x + 1][wrong_y-1],
                             workData[wrong_x+1][wrong_y], workData[wrong_x +1][wrong_y +1]]
                if neighboursOfSameColour(wrongColour, neighbours) < neighbourThreshold:
                    qualityErrors += 1
        
    return(qualityErrors)
                
    