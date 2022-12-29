# Provided code for Subdivison and Geodesic Spheres

# Philip Tarrer 
# Project 5

from __future__ import division
import traceback

# parameters used for object rotation by mouse
mouseX_old = 0
mouseY_old = 0
rot_mat = PMatrix3D()

V = [] # v table of vertices
G = [] # holds v elements 
O = {} # opposites table
currentCorner = 0
currentCornerVisible = False
randomColors = False
draw = False

# initalize things
def setup():
    size (800, 800, OPENGL)
    frameRate(30)
    noStroke()

# draw the current mesh (you will modify parts of this routine)
def draw():
    global G, V, O, currentCorner, currentCornerVisible, randomColors, draw
    randomSeed(0)
    background (100, 100, 180)    # clear the screen to black

    perspective (PI*0.2, 1.0, 0.01, 1000.0)
    camera (0, 0, 6, 0, 0, 0, 0, 1, 0)    # place the camera in the scene
    
    # create an ambient light source
    ambientLight (102, 102, 102)

    # create two directional light sources
    lightSpecular (202, 202, 202)
    directionalLight (100, 100, 100, -0.7, -0.7, -1)
    directionalLight (152, 152, 152, 0, 0, -1)
    
    pushMatrix();

    stroke (0)                    # draw polygons with black edges
    fill (200, 200, 200)          # set the polygon color to white
    ambient (200, 200, 200)
    specular (0, 0, 0)            # turn off specular highlights
    shininess (1.0)
    
    applyMatrix (rot_mat)   # rotate the object using the global rotation matrix

    # THIS IS WHERE YOU SHOULD DRAW YOUR MESH
    if (draw) :
        for c in range(0, len(V), 3) :
            if (randomColors):
                r = random(255)
                g = random(255)
                b = random(255)
                fill(r, g, b)
            else :
                fill(255, 255, 255)
            beginShape()
            vertex(G[V[c]][0], G[V[c]][1], G[V[c]][2])
            vertex(G[V[c+1]][0], G[V[c+1]][1], G[V[c+1]][2])
            vertex(G[V[c+2]][0], G[V[c+2]][1], G[V[c+2]][2])
            endShape(CLOSE)

            if (currentCornerVisible):
                pushMatrix()
                currentVert = PVector(G[V[currentCorner]][0], G[V[currentCorner]][1], G[V[currentCorner]][2])
                nextVert = PVector(G[V[nextCorner(currentCorner)]][0], G[V[nextCorner(currentCorner)]][1], G[V[nextCorner(currentCorner)]][2])
                prevVert = PVector(G[V[previousCorner(currentCorner)]][0], G[V[previousCorner(currentCorner)]][1], G[V[previousCorner(currentCorner)]][2])

                trans1 = PVector.mult(currentVert, 0.8)
                trans2 = PVector.mult(nextVert, 0.1)
                trans3 = PVector.mult(prevVert, 0.1)

                temp = PVector.add(trans1, trans2)
                temp = PVector.add(temp, trans3)

                translate(temp[0], temp[1], temp[2])
                sphere(0.1)
                popMatrix()
        popMatrix()
    

# read in a mesh file (this needs to be modified)
def read_mesh(filename):
    global G, V, O, currentCorner, currentCornerVisible, randomColors
    G = []
    V = []
    O = {}
    fname = "data/" + filename
    # read in the lines of a file
    with open(fname) as f:
        lines = f.readlines()

    # determine number of vertices (on first line)
    words = lines[0].split()
    num_vertices = int(words[1])
    print "number of vertices =", num_vertices

    # determine number of faces (on first second)
    words = lines[1].split()
    num_faces = int(words[1])
    print "number of faces =", num_faces

    # read in the vertices
    for i in range(num_vertices):
        words = lines[i+2].split()
        x = float(words[0])
        y = float(words[1])
        z = float(words[2])
        G.append((x, y, z))
        
        print "vertex: ", x, y, z

    # read in the faces
    for i in range(num_faces):
        j = i + num_vertices + 2
        words = lines[j].split()
        nverts = int(words[0])
        if (nverts != 3):
            print "error: this face is not a triangle"
            exit()

        index1 = int(words[1])
        index2 = int(words[2])
        index3 = int(words[3])
        V.append(index1)
        V.append(index2)
        V.append(index3)
        print "triangle: ", index1, index2, index3

    O = computeOTable(G, V)

# make sure proper error messages get reported when handling key presses
def keyPressed():
    try:
        handleKeyPressed()
    except Exception:
        traceback.print_exc()

# process key presses (call your own routines!)
def handleKeyPressed():
    global G, V, O, currentCorner, currentCornerVisible, randomColors, draw
    if key == '1':
        read_mesh ('tetra.ply')
        draw = True
    elif key == '2':
        read_mesh ('octa.ply')
        draw = True
    elif key == '3':
        read_mesh ('icos.ply')
        draw = True
    elif key == '4':
        read_mesh ('star.ply')
        draw = True
    elif key == 'n': # next
        currentCorner = nextCorner(currentCorner)
    elif key == 'p': # previous
        currentCorner = previousCorner(currentCorner)
    elif key == 'o': # opposite
        currentCorner = oppositeCorner(currentCorner)
    elif key == 's': # swing
        currentCorner = swingCorner(currentCorner)
    elif key == 'd': # subdivide mesh
        G, V, O = subdivision(G, V)
    elif key == 'i': # inflate mesh
        G = inflate(G)
    elif key == 'r': # toggle random colors
        randomColors = not randomColors
    elif key == 'c': # toggle showing current corner
        currentCornerVisible = not currentCornerVisible
    elif key == 'q': # quit the program
        exit()

# remember where the user first clicked
def mousePressed():
    global mouseX_old, mouseY_old
    mouseX_old = mouseX
    mouseY_old = mouseY

# change the object rotation matrix while the mouse is being dragged
def mouseDragged():
    global rot_mat
    global mouseX_old, mouseY_old
    
    if (not mousePressed):
        return
    
    dx = mouseX - mouseX_old
    dy = mouseY - mouseY_old
    dy *= -1

    len = sqrt (dx*dx + dy*dy)
    if (len == 0):
        len = 1
    
    dx /= len
    dy /= len
    rmat = PMatrix3D()
    rmat.rotate (len * 0.005, dy, dx, 0)
    rot_mat.preApply (rmat)

    mouseX_old = mouseX
    mouseY_old = mouseY

def nextCorner(cornerNumber):
    triangleNumber = cornerNumber // 3
    temp = (cornerNumber + 1) % 3
    return (3 * triangleNumber) + temp

def previousCorner(cornerNumber):
    triangleNumber = cornerNumber // 3
    temp = (cornerNumber - 1) % 3
    return (3 * triangleNumber) + temp

def oppositeCorner(cornerNumber):
    return O[cornerNumber]

def swingCorner(cornerNumber):
    return nextCorner(oppositeCorner(nextCorner(cornerNumber)))

def computeOTable(G, V):
    global O
    triples = []
    for i in range(len(V)) :
        triples.append([min(V[nextCorner(i)], V[previousCorner(i)]), max(V[nextCorner(i)], V[previousCorner(i)]), i])
    
    triples = sorted(triples)

    for i in range(0, len(triples), 2) :
        corner1 = triples[i][2]
        corner2 = triples[i + 1][2]
        O[corner1] = corner2
        O[corner2] = corner1
    return O

def subdivision(G, V):
    global O
    newO = O
    newVtab = []
    newGtab = G[:]
    midps = {}

    for a,b in newO.iteritems():
        if b > a :
            endp1 = G[V[previousCorner(a)]]
            endp2 = G[V[nextCorner(a)]]
            endvector1 = PVector(endp1[0], endp1[1], endp1[2])
            endvector2 = PVector(endp2[0], endp2[1], endp2[2])

            midp = PVector.add(endvector1, endvector2)
            midp = PVector.mult(midp, 0.5)

            midi = len(newGtab)
            newGtab.append(midp)
            midps[a] = midi
            midps[b] = midi
    
    
    for x in range(0, len(V), 3) :

        y = x + 1
        z = x + 2

        newVtab.extend([V[x], midps[z], midps[y], midps[z], V[y], midps[x], midps[y], midps[x], V[z], midps[x], midps[y], midps[z]])
    
    newO = computeOTable(newGtab, newVtab)
    return newGtab, newVtab, newO

def inflate(G) :
    newG = []
    for i in G :
        temp = PVector(i[0], i[1], i[2]).normalize()
        newG.append(temp)
    return newG
