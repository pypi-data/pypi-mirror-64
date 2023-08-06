from struct import unpack, calcsize
from sys import argv
from os.path import splitext
from os import listdir, getcwd, path
from numpy import zeros, complex_, abs, power, arange, concatenate, empty
from matplotlib import pyplot as plt

def readbin(input_files, save=False):
    noargs = len(input_files)

    if ( noargs == 0 ):
        print( "No filename specified." )
        exit()

    fh = open(input_files, 'rb' )
    print("Read file: "+input_files)
    header_raw = fh.read(calcsize("llllllliiddddddddddddddiidd"))
    header = unpack( "llllllliiddddddddddddddiidd", header_raw )
    nDims = header[3]
    nDimX = header[4]
    nDimY = header[5]
    nDimZ = header[6]
    bCmpx = header[8]
    t     = header[9]
    xMin  = header[10]
    xMax  = header[11]
    yMin  = header[12]
    yMax  = header[13]
    zMin  = header[14]
    zMax  = header[15]
    dx    = header[16]
    dy    = header[17]
    dz    = header[18]
    dkx   = header[19]
    dky   = header[20]
    dkz   = header[21]
    dt    = header[22]
    L     = header[25]
    T     = header[26]

    if ( header[0] != 1380 ):
        print( "Invalid file format." )
        exit()

    if ( bCmpx != 1 ):
        print( "File does not contain complex data." )
        exit()


    newfilename = splitext( input_files )[0] + ".mat"

    data_length = fh.seek(0,2)
    fh.seek(0,0)
    
    cmplxsize = calcsize("dd")

    if (nDims == 1):
        Nt = int(data_length/(header[0]+nDimX*cmplxsize)) #Number of time-steps in file
        data = zeros((nDimX,Nt),dtype=complex_)
        t = zeros(Nt)
        for n in range(0,Nt):
            fh.seek(n*(header[0]+nDimX*cmplxsize)) # go to beginning of file
            header_raw = fh.read(calcsize("llllllliiddddddddddddddiidd"))
            header = unpack( "llllllliiddddddddddddddiidd", header_raw )
            t[n] = header[9]
            fh.seek(n*(header[0]+nDimX*cmplxsize))
            fh.seek(header[0], 1) #skip header file relative to above position
            for i in range(0, nDimX): #read wave-function data
                rawcplxno = fh.read(cmplxsize)
                cmplxno = unpack( "dd", rawcplxno )
                data[i,n] = complex(cmplxno[0],cmplxno[1])
        if save == True:
            import scipy.io as sio
            sio.savemat(newfilename, mdict={'wavefunction': data, 'nDims': nDims, 'nDimX': nDimX, 'xMin': xMin, 'xMax': xMax, 'dx': dx, 'L': L, 'T': T, 't': t} )
            print(newfilename+" created.")

        return {'wavefunction': data, 'nDims': nDims, 'nDimX': nDimX, 'xMin': xMin, 'xMax': xMax, 'dx': dx, 'L': L, 'T': T, 't': t}

    if (nDims == 2):
        Nt = int(data_length/(header[0]+nDimX*nDimY*cmplxsize)) #Number of time-steps in file
        data = zeros((nDimX,nDimY,Nt),dtype=complex_) 
        t = zeros(Nt)
        for n in range(0,Nt):
            fh.seek(n*(header[0]+nDimX*nDimY*cmplxsize)) # go to beginning of file
            header_raw = fh.read(calcsize("llllllliiddddddddddddddiidd"))
            header = unpack( "llllllliiddddddddddddddiidd", header_raw )
            t[n] = header[9]
            fh.seek(n*(header[0]+nDimX*nDimY*cmplxsize))
            fh.seek(header[0], 1) #skip header file relative to above position
            for i in range(0, nDimX):
                for j in range(0, nDimY):
                    rawcplxno = fh.read(cmplxsize)
                    cmplxno = unpack( "dd", rawcplxno )
                    data[j,i,n] = complex(cmplxno[0],cmplxno[1])
        if save == True:
            import scipy.io as sio
            sio.savemat(newfilename, mdict={'wavefunction': data, 'nDims': nDims, 'nDimX': nDimX, 'nDimY': nDimY, 'xMin': xMin, 'yMin': yMin, 'xMax': xMax, 'yMax': yMax, 'dx': dx, 'dy': dy, 'L': L, 'T': T, 't': t} )
            print(newfilename+" created.")
        return {'wavefunction': data, 'nDims': nDims, 'nDimX': nDimX, 'nDimY': nDimY, 'xMin': xMin, 'yMin': yMin, 'xMax': xMax, 'yMax': yMax, 'dx': dx, 'dy': dy, 'L': L, 'T': T, 't': t}
            
    if (nDims == 3):
        Nt = int(data_length/(header[0]+nDimX*nDimY*nDimZ*cmplxsize)) #Number of time-steps in file
        data = zeros((nDimX,nDimY,nDimZ,Nt),dtype=complex_) 
        t = zeros(Nt)
        for n in range(0,Nt):
            fh.seek(n*(header[0]+nDimX*nDimY*nDimZ*cmplxsize)) # go to beginning of file
            header_raw = fh.read(calcsize("llllllliiddddddddddddddiidd"))
            header = unpack( "llllllliiddddddddddddddiidd", header_raw )
            t[n] = header[9]
            fh.seek(n*(header[0]+nDimX*nDimY*nDimZ*cmplxsize))
            fh.seek(header[0], 1) #skip header file relative to above position
            for i in range(0, nDimX):
                for j in range(0, nDimY):
                    for k in range(0, nDimZ):
                        rawcplxno = fh.read(cmplxsize)
                        cmplxno = unpack( "dd", rawcplxno )
                        data[k,j,i,n] = complex(cmplxno[0],cmplxno[1])
        if save == True:
            import scipy.io as sio
            sio.savemat(newfilename, mdict={'wavefunction': data, 'nDims': nDims, 'nDimX': nDimX, 'nDimY': nDimY, 'xMin': xMin, 'yMin': yMin, 'xMax': xMax, 'yMax': yMax, 'dx': dx, 'dy': dy, 'L': L, 'T': T, 't': t} )
            print(newfilename+" created.")
        return {'wavefunction': data, 'nDims': nDims, 'nDimX': nDimX, 'nDimY': nDimY, 'xMin': xMin, 'yMin': yMin, 'xMax': xMax, 'yMax': yMax, 'dx': dx, 'dy': dy, 'L': L, 'T': T, 't': t}
        
    fh.close()

def readall(n_int_state, directory=path.abspath(getcwd()), save=False):
    # search, read and append data
    file_list = []
    file_list = [f for f in listdir(directory) if f.endswith(str(n_int_state)+'.bin')]
    data = []
    for i in range(0, len(file_list)):
        data.append(readbin(file_list[i]))

    # concatenate psi and time
    psi = data[0]["wavefunction"]
    t = data[0]["t"]
    for i in range(1, len(file_list)):
        t = concatenate((t, data[i]["t"]))
        psi = concatenate((psi, data[i]["wavefunction"]), axis=data[0]["nDims"])

    # sort after time
    sorted_inds = t.argsort()
    sorted_t = empty(shape=t.shape)
    sorted_psi = empty(shape=psi.shape,dtype=complex_)
    if data[0]["nDims"] == 1:
        for i in range(0, len(t)):
            sorted_psi[:,i] = psi[:,sorted_inds[i]]
            sorted_t[i] = t[sorted_inds[i]]
        if save == True:
            import scipy.io as sio
            newfilename = directory + str(n_int_state) + ".mat"
            sio.savemat(newfilename, mdict={'wavefunction': psi, 'nDims': data[0]["nDims"], 'nDimX': data[0]["nDimX"], 'xMin': data[0]["xMin"], 'xMax': data[0]["xMax"], 'dx': data[0]["dx"], 'L': data[0]["L"], 'T': data[0]["T"], 't': t} )
            print(newfilename+" created.")

        return {'wavefunction': psi, 'nDims': data[0]["nDims"], 'nDimX': data[0]["nDimX"], 'xMin': data[0]["xMin"], 'xMax': data[0]["xMax"], 'dx': data[0]["dx"], 'L': data[0]["L"], 'T': data[0]["T"], 't': t}


    if data[0]["nDims"] == 2:
        for i in range(0, len(t)):
            sorted_psi[:,:,i] = psi[:,:,sorted_inds[i]]
            sorted_t[i] = t[sorted_inds[i]]
        if save == True:
            import scipy.io as sio
            newfilename = directory + str(n_int_state) + ".mat"
            sio.savemat(newfilename, mdict={'wavefunction': psi, 'nDims': data[0]["nDims"], 'nDimX': data[0]["nDimX"], 'nDimY': data[0]["nDimY"], 'xMin': data[0]["xMin"], 'yMin': data[0]["yMin"], 'xMax': data[0]["xMax"], 'yMax': data[0]["yMax"], 'dx': data[0]["dx"], 'dy': data[0]["dy"], 'L': data[0]["L"], 'T': data[0]["T"], 't': t} )
            print(newfilename+" created.")
        return {'wavefunction': psi, 'nDims': data[0]["nDims"], 'nDimX': data[0]["nDimX"], 'nDimY': data[0]["nDimY"], 'xMin': data[0]["xMin"], 'yMin': data[0]["yMin"], 'xMax': data[0]["xMax"], 'yMax': data[0]["yMax"], 'dx': data[0]["dx"], 'dy': data[0]["dy"], 'L': data[0]["L"], 'T': data[0]["T"], 't': t} 

    if data[0]["nDims"] == 3:
        for i in range(0, len(t)):
            sorted_psi[:,:,:,i] = psi[:,:,:,sorted_inds[i]]
            sorted_t[i] = t[sorted_inds[i]]
        if save == True:
            import scipy.io as sio
            newfilename = directory + str(n_int_state) + ".mat"
            sio.savemat(newfilename, mdict={'wavefunction': psi, 'nDims': data[0]["nDims"], 'nDimX': data[0]["nDimX"], 'nDimY': data[0]["nDimY"], 'nDimZ': data[0]["nDimZ"], 'xMin': data[0]["xMin"], 'yMin': data[0]["yMin"], 'zMin': data[0]["zMin"], 'xMax': data[0]["xMax"], 'yMax': data[0]["yMax"], 'zMax': data[0]["zMax"], 'dx': data[0]["dx"], 'dy': data[0]["dy"], 'dz': data[0]["dz"], 'L': data[0]["L"], 'T': data[0]["T"], 't': t} )
            print(newfilename+" created.")
        return {'wavefunction': psi, 'nDims': data[0]["nDims"], 'nDimX': data[0]["nDimX"], 'nDimY': data[0]["nDimY"], 'nDimZ': data[0]["nDimZ"], 'xMin': data[0]["xMin"], 'yMin': data[0]["yMin"], 'zMin': data[0]["zMin"], 'xMax': data[0]["xMax"], 'yMax': data[0]["yMax"], 'zMax': data[0]["zMax"], 'dx': data[0]["dx"], 'dy': data[0]["dy"], 'dz': data[0]["dz"], 'L': data[0]["L"], 'T': data[0]["T"], 't': t}


def plotbin(filename):
    data = readbin(filename)
    if data["nDims"]==1:
        x = arange(data["xMin"], data["xMax"], data["dx"])
        psi2 = abs(power(data["wavefunction"][:,0],2))
        plt.ylabel(r"$|\Psi |^2$")
        plt.xlabel("position")
        plt.plot(x, psi2, label="t="+str(data["t"][0]))
        plt.xlim(data["xMin"], data["xMax"])
        plt.grid()
        plt.legend()
        plt.tight_layout()
        plt.savefig(filename+".png")
        print(filename+".png has been created.")
        plt.close()

    if data["nDims"]==2:
        x = arange(data["xMin"], data["xMax"], data["dx"])
        y = arange(data["yMin"], data["yMax"], data["dy"])
        psi2= abs(power(data["wavefunction"][:,:,0],2))
        plt.title(r"$|\Psi |^2$ at t="+str(data["t"][0]))
        plt.ylabel("y")
        plt.xlabel("x")
        plt.pcolormesh(x, y, psi2)
        plt.grid()
        plt.tight_layout()
        plt.savefig(filename+".png")
        print(filename+".png has been created.")
        plt.close()


if __name__ == '__main__':
    for i in range(1, len(argv)):
        readbin(argv[i], save=True)