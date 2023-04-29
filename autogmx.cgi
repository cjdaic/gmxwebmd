#!C:/Users/CJ/AppData/Local/Programs/Python/Python39/python.exe
# -*- coding: utf-8 -*-

import sys
import subprocess
import json
from time import sleep
import configparser
import cgi

sys.stdout.write("Content-Type: text/plain\n\n")


def autorun(command):
    result = ""
    command  = "bash -c '{}'".format(command)
    process = subprocess.run(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout = str(process.stdout.decode("utf-8"))
    stderr = str(process.stderr.decode("utf-8"))
    result += stdout
    result += stderr

    sys.stdout.write(result)
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

cd_grep = "grep -v  HOH " + usr_dir + "temp.pdb > " + usr_dir + "temp_clean.pdb"
if usr_data.get("ignh"):
    ignh = " -ignh"
else :
    ignh = ""
cd_pdb2gmx = "gmx pdb2gmx -f " + usr_dir + "temp_clean.pdb -o " + usr_dir + "temp_processed.gro -ff " + usr_data.get("forcefield") + " -water " + usr_data.get("waterbox") + ignh

if usr_data.get("ct"):
    ct = " -c"
else :
    ct = ""


cd_editconf = "gmx editconf -f " + usr_dir + "temp_processed.gro -o " + usr_dir + "temp_newbox.gro " + ct + " -d " + usr_data.get("dst") + " -bt " + usr_data.get("bt")

cd_solvate = "gmx solvate -cp " + usr_dir + "temp_newbox.gro -cs " + usr_data.get("cs") + " -o " + usr_dir + "temp_solv.gro -p " + usr_dir + "topol.top"

cd_grompp = "gmx grompp -f " + usr_dir + "ions.mdp -c " + usr_dir + "temp_solv.gro -p " + usr_dir + "topol.top -o " + usr_dir + "ions.tpr"

cd_genion = "gmx genion -s " + usr_dir + "ions.tpr -o " + usr_dir + "temp_solv_ions.gro -p " + usr_dir + "topol.top -pname NA -nname CL -neutral"

cd_mdrun = "gmx mdrun -v -deffnm em"

cd_energy = "gmx energy -f " + usr_dir + "em.edr -o " + usr_dir + "potential.xvg"

cd_grompp_nvt = "gmx grompp -f " + usr_dir + "nvt.mdp -c " + usr_dir + "em.gro -r " + usr_dir + "em.gro -p " + usr_dir + "topol.top -o " + usr_dir + "nvt.tpr"

cd_mdrun_nvt = "gmx mdrun -deffnm nvt"

cd_energy_nvt = "gmx energy -f " + usr_dir + "nvt.edr -o " + usr_dir + "temperature.xvg"

cd_grompp_npt = "gmx grompp -f " + usr_dir + "npt.mdp -c " + usr_dir + "nvt.gro -r " + usr_dir + "nvt.gro -t " + usr_dir + "nvt.cpt -p " + usr_dir + "topol.top -o " + usr_dir + "npt.tpr"

cd_mdrun_npt = "gmx mdrun -deffnm npt"

cd_energy_npt = "gmx energy -f " + usr_dir + "npt.edr -o " + usr_dir + "pressure.xvg"

cd_energy_density = "gmx energy -f " + usr_dir + "npt.edr -o " + usr_dir + "density.xvg"

cd_grompp_md = "gmx grompp -f " + usr_dir + "md.mdp -c " + usr_dir + "npt.gro -t " + usr_dir + "npt.cpt -p " + usr_dir + "topol.top -o " + usr_dir + "md_0_1.tpr"

cd_mdrun_md = "gmx mdrun -deffnm md_0_1"
#params to be added
cd_trjconv = "gmx trjconv -s " + usr_dir + "md_0_1.tpr -f " + usr_dir + "md_0_1.xtc -o " + usr_dir + "md_0_1_noPBC.xtc -pbc mol -center"

cd_rms = "gmx rms -s " + usr_dir + "md_0_1.tpr -f " + usr_dir + "md_0_1_noPBC.xtc -o " + usr_dir + "rmsd.xvg -tu ns"

cd_rms_s = "gmx rms -s " + usr_dir + "em.tpr -f " + usr_dir + "md_0_1_noPBC.xtc -o " + usr_dir + "rmsd_xtal.xvg -tu ns"

cd_gyrate = "gmx gyrate -s " + usr_dir + "md_0_1.tpr -f " + usr_dir + "md_0_1_noPBC.xtc -o " + usr_dir + "gyrate.xvg"
#...

def modify_mdp(file: str):
    config = configparser.ConfigParser(inline_comment_prefixes=";")
    config.read(file, encoding='utf-8')
    config.set("md", "nstep", str(usr_data.get("nstep")))
    with open(file, 'w') as f:
        config.write(f)

def gmx_inital():
    autorun(cd_grep)
    autorun(cd_pdb2gmx)
    autorun(cd_editconf)
    autorun(cd_solvate)
    autorun(cd_genion)
    autorun(cd_grompp)
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
    gmx_inital()
    nvt_npt()
    md()


main()


