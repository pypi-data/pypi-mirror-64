#merge ts files
from pathlib import Path 
import sys 
import os
import shutil
from concurrent.futures import ThreadPoolExecutor,wait,ALL_COMPLETED
import time
import click
import hashlib
import requests
def down_content(url,outfile,downloader,rate = ''):
    if outfile.exists():
        print(outfile,'Exists',rate)
        return
    else:
        print('{:4.2}%'.format(rate*100),'downloading',url,outfile.name)
    temp_file = outfile.with_suffix('.temp_download')
    content = downloader.get(url, stream=True)
    with open(temp_file, "wb") as fp:
        for chunk in content.iter_content(chunk_size=512):
            fp.write(chunk)
    os.rename(temp_file,outfile)
def _deal(s):
    if not s.startswith('#'):
        return s.strip()
    else:
        start = s.find('URI=')
        if start != -1:
            keyf = s[start+4:].strip().replace('"','')
            return keyf.strip()
    return None
def download_m3u8_requeset(url,out_name,delete_m3u8,suffix,multi_requests):
    
    if out_name.exists():
        print(url,out_name,"文件已存在")
        return
    else:
        print('download',url,out_name)
    m3u8_dir = out_name.parent / (out_name.name + '_dir')
    if not m3u8_dir.exists():
        os.makedirs(m3u8_dir)
    m3u8_file = m3u8_dir / 'index.m3u8'

    session = requests.session()

    down_content(url,m3u8_file,session)
    url_dir = url[:url.rindex('/')+1]
    files = []
    for i in open(m3u8_file):
        s = _deal(i)
        if s:
            files.append(s)
    pool = ThreadPoolExecutor(multi_requests)
    pwd = os.getcwd()
    os.chdir(m3u8_dir)
    n_files = len(files)
    all_tasks = [pool.submit(down_content,url_dir + i,Path(i),session,n/n_files) for n,i in enumerate(files)]
    wait(all_tasks,return_when=ALL_COMPLETED)
    time.sleep(1)
    os.system(f'ffmpeg -y -allowed_extensions ALL -i index.m3u8 -c copy -movflags faststart "{out_name}"')
    os.chdir(pwd)
    n_exists_files = len(list(m3u8_dir.glob('*')))
    if delete_m3u8 and n_exists_files>n_files:
        shutil.rmtree(m3u8_dir)


def download_m3u8_ffmpeg(url,out_name,delete_m3u8,suffix,multi_requests):

    if out_name.exists():
        print(url,out_name,"文件已存在")
        return
    else:
        print('download',url,out_name)
    m3u8_dir = out_name.parent / (out_name.name + '_dir')
    if not m3u8_dir.exists():
        os.makedirs(m3u8_dir)
    m3u8_name = m3u8_dir / ('temp.m3u8')
    os.system(f'ffmpeg -y -i {url} -c copy  {m3u8_name}')
    time.sleep(0.5)
    fs = list(m3u8_dir.glob('*.ts'))
    outfile = merge_file(fs,m3u8_dir/'m3u8.txt')
    os.system('ffmpeg -y -allowed_extensions ALL -i "{}" -c copy -movflags faststart "{}"'.format(outfile,out_name))
    if delete_m3u8:
        shutil.rmtree(m3u8_dir)
def merge_file(files,outfile='out.txt',key_file = None):
    file_list = [Path(i).absolute() for i in files]
    stem = file_list[0].stem
    ipos = 0
    for i in range(1,len(stem)+1):
        print(stem[-i])
        if not stem[-i].isdigit():
            ipos = len(stem) - (i-1)
            break
    print(ipos,'ipos')
    file_list.sort(key = lambda x:int(x.stem[ipos:]))
    fp = open(outfile,'w')
    fp.write('#EXTM3U\n#EXT-X-TARGETDURATION:400\n')
    sf = '#EXTINF:400,\n{}\n'
    if key_file is not None:
        fp.write('#EXT-X-KEY:METHOD=AES-128,URI="{}"\n'.format(key_file))
    
    for f in file_list:
        fp.write(sf.format(f))
    fp.write('#EXT-X-ENDLIST')
    fp.close()
    return outfile 
def deal_dir(dirname,format='*.ts',walk=True,out_dir=None,key_f = '*.key',used_dirs = [],fast=True):
    p = Path(dirname)
    if str(p) in used_dirs:
        return
    try:
        fs = list(p.glob(format))
    except:
        return
    key_file = list(p.glob(key_f))
    if key_file:
        key_file = key_file[0]
    else:
        key_file = None
    if fs:
        used_dirs.append(str(p))
        if out_dir is None:
            out_dir = p
        else: 
            out_dir = Path(out_dir)
        outfile = out_dir / (p.stem+'_out.m3u8')
        merge_file(fs,outfile,key_file=key_file)

        out_mp4 = out_dir / outfile.with_suffix('.mp4').name
        print(out_mp4)
        if not out_mp4.exists() or True:
            if fast is True:
                out_mp4 = out_mp4.with_suffix('.fast.mp4')
            os.system('ffmpeg -y -allowed_extensions ALL -i "{}" -c copy -movflags faststart "{}"'.format(outfile,out_mp4))
        if out_mp4.is_file():
            os.remove(outfile)
    else:
        m3u8_files = list(p.glob('*.m3u8'))
        if m3u8_files:
            for i in m3u8_files:
                outfile,m3u8_dir = merge_m3u8_file(i)
                if m3u8_dir:
                    used_dirs.append(str(m3u8_dir))
                    if out_dir is None:
                        out_dir = p
                    else: 
                        out_dir = Path(out_dir)
                    out_mp4 = out_dir / outfile.with_suffix('.mp4').name
                    if not out_mp4.exists() or True:
                        if fast is True:
                            out_mp4 = out_mp4.with_suffix('.fast.mp4')
                        os.system('ffmpeg -y -allowed_extensions ALL -i "{}" -c copy -movflags faststart "{}"'.format(outfile,out_mp4))
                    if out_mp4.is_file():
                        os.remove(outfile)
    if walk:
        for i in p.glob('*'):
            if i.is_dir():
                deal_dir(i,format,walk,out_dir)
def merge_m3u8_file(m3u8_name):
    m3u8_parent = Path(m3u8_name).parent
    fp = open(m3u8_name)
    ts_path = None
    for i in fp:
        if not i.startswith('#'):
            try:
                ts_path = Path(i)
            except:
                continue
            break 
    fp.seek(0,0)
    ts_dir = None
    if ts_path is None:
        return None,None
    for i in range(100):
        name = ts_path.name
        ts_path = ts_path.parent 
        if (m3u8_parent / name).exists():
            ts_dir = m3u8_parent/name
            break
    else:
        print('no ts file was found.')
        return None,None
    out_m3u8 = None
    if ts_dir:
        out_m3u8 = ts_dir/(ts_dir.name+'.m3u8')
        ofp = open(out_m3u8,'w')
        for i in fp:
            if i.startswith('#'):
                start = i.find('URI=')
                if start != -1:
                    keyf = i[start+4:].strip().replace('"','')
                    m = Path(keyf)
                    keyn = ts_dir / m.name 
                    i = '{}"file://{}"\n'.format(i[:start+4],keyn)
                ofp.write(str(i))
            else:
                ofp.write(str(ts_dir/Path(i).name))
        ofp.close()
    return out_m3u8,ts_dir
@click.command()
@click.option('--dirname','-d',default=None,help="需要合并的m3u8文件所在的文件夹")
@click.option('--suffix','-s',default='.ts',help='视频文件后缀')
@click.option('--url','-u',help='需要下载的m3u8链接,如果url采用多行的形式则认为是多个url，如果单个url采用空格分割，则分别认定为url output')
@click.option('--output','-o',help='输出文件,%d作为格式化文件名输出。m3u8文件合并时，该参数为文件夹路径')
@click.option('--multi','-m',default=1,help='下载m3u8时是否采用多线程（同时下载多个url）')
@click.option('--delete','-D',default=True,type=click.BOOL,help='是否删除源文件,针对url下载项使用')
@click.option('--downloader',default='requests',type=click.Choice(['requests','ffmpeg']),help='m3u8 下载器选择(默认requests)')
@click.option('--multi_requests',default=1,help='requests 下载单个url的线程数')
def main(dirname=None,url=None,suffix='.ts',output=None,multi=1,delete=False,downloader='requests',multi_requests=1):
    suffix = '*'+suffix
    if url:
        if Path(url).is_file():
            url = open(url).read()
        if multi > 1:
            po = ThreadPoolExecutor(multi)
        else:
            po = None
        if downloader == 'ffmpeg':
            download_m3u8 = download_m3u8_ffmpeg 
        else:
            download_m3u8 = download_m3u8_requeset
        for i,s in enumerate(url.strip().split('\n')):
            st = s.split()
            url = st[0]
            if len(st) == 1:
                out_name = '{}.fast.mp4'.format(hashlib.md5(st[0].encode('utf8')).hexdigest())
            else:
                out_name = st[1]
            
            if output:
                out_name = output.replace('%d',str(i))
            else:
                if out_name.find('.') == -1:
                    out_name = out_name + '.fast.mp4'
            out_name = Path(out_name).absolute()
            if po is not None:
                po.submit(download_m3u8,url,out_name,delete,suffix,multi_requests)
            else:
                download_m3u8(url,out_name,delete,suffix,multi_requests)

    if dirname:
        deal_dir(dirname,format=suffix,out_dir=output,fast=True)
if __name__=='__main__':
    
    main()