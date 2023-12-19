import hashlib
import numpy as np
from time import time
from mpi4py import MPI

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def brute_force(saved, leng, arr):
    
    t0 = time()
    f = 0
    i = 0
    tim = 0
    found = None
    while f == 0 and i < len(arr) :
        password = str(arr[i]).zfill(leng)
        hashed_password = hash_password(password)
        if hashed_password == saved:

            f = 1
            found = password
            # print(f"Found password: {password}")
            t1 = time()
            tim = t1-t0
            # print('time = {}'.format(tim))
        i += 1
    return tim, found

def guess_time(leng, arr, passw=None):
    pass_len = leng
    correct = passw

    saved_password = hash_password(str(correct).zfill(pass_len))
        
    td, found = brute_force(saved_password, pass_len, arr)
    return td, found, correct

# mpiexec -n 2 python passw.py

pass_len=5
comm = MPI.COMM_WORLD
id = comm.Get_rank()
numtreads = comm.Get_size()


ens = 1
tt = 0
for i in range(ens):
    if(id == 0):
        t0_0 = time()
        data = np.arange(10**pass_len)
        data = np.array_split(data, numtreads)
        # PASSWORD = 0
        # PASSWORD = int(10**pass_len/2)
        PASSWORD = np.random.randint(0,10**(pass_len), dtype='int32')
        # chunk = np.random.randint(0,numtreads, dtype='int32')
        # PASSWORD = data[chunk][len(data[chunk])//2]
        if i==0:
            print(pass_len, ens, PASSWORD)
    else:
        data = None
        PASSWORD = None
    
    data = comm.scatter(data)
    PASSWORD = comm.bcast(PASSWORD)


    ans = guess_time(pass_len, data, PASSWORD)
    if(type(ans[1]) is str):
        tt += ans[0]
ttt = comm.reduce(tt, MPI.SUM, root=0)
if(id==0):
    print('\ntime = {}'.format(ttt/ens))
    
