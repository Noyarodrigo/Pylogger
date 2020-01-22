import file_funcs as ff
import multiprocessing

lk_file = multiprocessing.Lock()

ff.reader_full(lk_file)
