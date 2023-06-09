#!C:\Users\CJ\AppData\Local\Programs\Python\Python39\python.exe
# -*- coding: utf-8 -*-

import sys
import subprocess
import json
from time import sleep
import configparser
import cgi
import os
sys.stdout.write("Content-Type: text/plain\n\n")

def start():
    os.chdir("D:/apache/Apache24/htdocs/usr")
def autorun(command):
    result = ""
    command  = "bash -c '{}'".format(command)
    process = subprocess.run(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout = str(process.stdout.decode("utf-8"))
    stderr = str(process.stderr.decode("utf-8"))
    result += stdout
    result += stderr
    if 'error' in result:
        
        sys.stdout.write(stdout + stderr)
        exit()
    result = command + "\n"
    print(command)
    print(stderr)
    sys.stdout.write(result)
    sys.stdout.flush()
    sleep(5)

#打开/usr/usr.json文件
with open("D:\\apache\\Apache24\\htdocs\\usr\\usr.json","r",encoding='utf-8') as usr_conf:
    f = usr_conf.read()
    usr_data = json.loads(f)
#根据json文件读取用户名与各项参数，生成用户的文件目录，在里面生成gromacs所需的各项文件
###
#dir = usr_data.get("name")
#cd_mkdir = "mkdir " + dir
#cd_cd = "cd " +dir

#gromacs脚本
usr_dir = "/mnt/d/apache/Apache24/htdocs/usr/"
log_dir = "log/"

cd_grep = "grep -v  HOH temp.pdb > temp_clean.pdb"
if usr_data.get("ignh"):
    ignh = " -ignh"
else :
    ignh = ""
cd_pdb2gmx = "gmx pdb2gmx -f  temp_clean.pdb -o  temp_processed.gro -ff " + usr_data.get("forcefield") + " -water " + usr_data.get("waterbox") + ignh + " -p topol.top > " + log_dir + "pdb2gmx.log"

if usr_data.get("ct"):
    ct = " -c"
else :
    ct = ""



cd_editconf = "gmx editconf -f  temp_processed.gro -o  temp_newbox.gro " + ct + " -d " + usr_data.get("dst") + " -bt " + usr_data.get("bt") + " > " + log_dir + "editconf.log"

cd_solvate = "gmx solvate -cp  temp_newbox.gro -cs " + usr_data.get("cs") + " -o  temp_solv.gro -p  topol.top > " + log_dir + "solvate.log"

cd_grompp = "gmx grompp -f  ions.mdp -c  temp_solv.gro -p  topol.top -o ions.tpr > " + log_dir + "grompp.log"

cd_grompp_em = "gmx grompp -f minim.mdp -c temp_solv_ions.gro -p topol.top -o em.tpr > " + log_dir + "grompp_em.log"

cd_genion = "gmx genion -s  ions.tpr -o  temp_solv_ions.gro -p  topol.top -pname NA -nname CL -neutral < genion.txt > " + log_dir + "genion.log"

cd_mdrun = "gmx mdrun -v -deffnm em < mdrun.txt > " + log_dir + "mdrun.log"

cd_energy = "gmx energy -f  em.edr -o  potential.xvg > " + log_dir + "energy.log"

cd_grompp_nvt = "gmx grompp -f  nvt.mdp -c  em.gro -r  em.gro -p  topol.top -o  nvt.tpr > " + log_dir + "grompp_nvt.log"

cd_mdrun_nvt = "gmx mdrun -deffnm nvt < mdrun.txt > " + log_dir + "mdrun_nvt.log"

cd_energy_nvt = "gmx energy -f  nvt.edr -o  temperature.xvg > " + log_dir + "energy_nvt.log"

cd_grompp_npt = "gmx grompp -f  npt.mdp -c  nvt.gro -r  nvt.gro -t  nvt.cpt -p  topol.top -o  npt.tpr > " + log_dir + "grompp_npt.log"

cd_mdrun_npt = "gmx mdrun -deffnm npt < mdrun.txt > " + log_dir + "mdrun_npt.log"

cd_energy_npt = "gmx energy -f  npt.edr -o  pressure.xvg > " + log_dir + "energy_npt.log"

cd_energy_density = "gmx energy -f  npt.edr -o  density.xvg > " + log_dir + "energy_density.log"

cd_grompp_md = "gmx grompp -f  md.mdp -c  npt.gro -t  npt.cpt -p  topol.top -o  md_0_1.tpr > " + log_dir + "grompp_md.log"

cd_mdrun_md = "gmx mdrun -deffnm md_0_1 > " + log_dir + "mdrun_md.log"
#params to be added
cd_trjconv = "gmx trjconv -s  md_0_1.tpr -f  md_0_1.xtc -o  md_0_1_noPBC.xtc -pbc mol -center > " + log_dir + "trjconv.log"

cd_rms = "gmx rms -s  md_0_1.tpr -f  md_0_1_noPBC.xtc -o  rmsd.xvg -tu ns > " + log_dir + "rms.log"

cd_rms_s = "gmx rms -s  em.tpr -f  md_0_1_noPBC.xtc -o  rmsd_xtal.xvg -tu ns > " + log_dir + "rms_s.log"

cd_gyrate = "gmx gyrate -s  md_0_1.tpr -f  md_0_1_noPBC.xtc -o  gyrate.xvg > " + log_dir + "gyrate.log"
#...
def genion():
    with open("genion.txt", "r+") as file:
        lines = file.readlines()
        lines[0] = usr_data.get("groups")
        file.seek(0)
        file.writelines(lines)
def grompp():
    with open("mdrun.txt", "r+") as file:
        lines = file.readlines()
        lines[0] = usr_data.get("selections")
        file.seek(0)
        file.writelines(lines)
def modify_mdp(file: str):
    config = configparser.ConfigParser(inline_comment_prefixes=";")
    config.read(file, encoding='utf-8')
    config.set("md", "nstep", str(usr_data.get("nstep")))
    with open(file, 'w') as f:
        config.write(f)
def gmx_inital():
    genion()
    grompp()
    autorun(cd_grep)
    autorun(cd_pdb2gmx)
    autorun(cd_editconf)
    autorun(cd_solvate)
    autorun(cd_grompp)
    autorun(cd_genion)
    autorun(cd_grompp_em)
    autorun(cd_mdrun)
    autorun(cd_energy)
    #提示用户完成初始化 tobeadded，在底部框中给出生成文件链接供客户端下载,接下来修改mdp文件
    #modify_mdp("ions.mdp")
    

def nvt_npt():    
    #modify_mdp("nvt.mdp")
    #modify_mdp("npt.mdp")
    autorun(cd_grompp_nvt)
    autorun(cd_mdrun_nvt)
    autorun(cd_energy_nvt)
    autorun(cd_grompp_npt)
    autorun(cd_mdrun_npt)
    autorun(cd_energy_npt)
    autorun(cd_energy_density)

    #提示用户完成分析 tobeadded，在底部框中给出生成文件链接供客户端下载，接下来修改其他mdp文件


def md():
    #modify_mdp("md.mdp")
    autorun(cd_grompp_md)
    autorun(cd_mdrun_md)
    autorun(cd_trjconv)
    autorun(cd_rms)
    autorun(cd_rms_s)
    autorun(cd_gyrate)

    #提示完成md，点击跳转标签查看xvg等分析文件，在底部框中给出生成文件链接供客户端下载

def main():
    #根据网页读取的json修改各个命令行，每隔10秒自动执行指令，并输出运行的result，修改mdp文件，以及自动执行
    #modify_mdp("usr/ions.mdp")
    start()
    gmx_inital()
    nvt_npt()
    md()


main()


