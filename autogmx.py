#!usr/bin/python

import sys
import subprocess
import json
from time import sleep
import configparser

result = ""

def autorun(command):
    result += subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    sleep(10)


#打开/usr/usr.json文件
with open("/usr/usr.json","r") as usr_conf:
    usr_data = json.loads(usr_conf)
#根据json文件读取用户名与各项参数，生成用户的文件目录，在里面生成gromacs所需的各项文件
dir = usr_data.get("name")
cd_mkdir = "mkdir " + dir
cd_cd = "cd " +dir
#gromacs脚本
if usr_data.get("ignh"):
    ignh = " -ignh"
else :
    ignh = ""
cd_pdb2gmx = "gmx pdb2gmx -f temp.pdb -o temp_processeud.gro -ff" + usr_data.get("ff") + "-water" + usr_data.get("wt") + ignh

if usr_data.get("ct"):
    ct = " -c"
else :
    ct = ""
cd_editconf = "gmx editconf -f temp_processed.gro -o temp_newbox.gro " + ct + "-d " + usr_data.get("dst") + " -bt" + usr_data.get("bt")

cd_solvate = "gmx solvate -cp temp_newbox.gro -cs " + usr_data.get("cs") + " -o temp_solv.gro -p topol.top"

cd_grompp = "gmx grompp -f ions.mdp -c temp_solv.gro -p topol.top -o ions.tpr"

cd_genion = "gmx genion -s ions.tpr -o temp_solv_ions.gro -p topol.top -pname NA -nname CL -neutral"

cd_mdrun = "gmx mdrun -v -deffnm em"

cd_energy = "gmx energy -f em.edr -o potential.xvg"

cd_grompp_nvt = "gmx grompp -f nvt.mdp -c em.gro -r em.gro -p topol.top -o nvt.tpr"

cd_mdrun_nvt = "gmx mdrun -deffnm nvt"

cd_energy_nvt = "gmx energy -f nvt.edr -o temperature.xvg"

cd_grompp_npt = "gmx grompp -f npt.mdp -c nvt.gro -r nvt.gro -t nvt.cpt -p topol.top -o npt.tpr"

cd_mdrun_npt = "gmx mdrun -deffnm npt"

cd_energy_npt = "gmx energy -f npt.edr -o pressure.xvg"

cd_energy_density = "gmx energy -f npt.edr -o density.xvg"

cd_grompp_md = "gmx grompp -f md.mdp -c npt.gro -t npt.cpt -p topol.top -o md_0_1.tpr"

cd_mdrun_md = "gmx mdrun -deffnm md_0_1"
#params to be added
cd_trjconv = "gmx trjconv -s md_0_1.tpr -f md_0_1.xtc -o md_0_1_noPBC.xtc -pbc mol -center"

cd_rms = "gmx rms -s md_0_1.tpr -f md_0_1_noPBC.xtc -o rmsd.xvg -tu ns"

cd_rms_s = "gmx rms -s em.tpr -f md_0_1_noPBC.xtc -o rmsd_xtal.xvg -tu ns"

cd_gyrate = "gmx gyrate -s md_0_1.tpr -f md_0_1_noPBC.xtc -o gyrate.xvg"
#...

def modify_mdp(file: str):
    config = configparser.ConfigParser(inline_comment_prefixes=";")
    config.read(file)
    config.set("md", "nstep", str(usr_data.get("nstep")))
    with open(file, 'w') as f:
        config.write(f)

def gmx_inital():
    autorun(cd_pdb2gmx)
    autorun(cd_editconf)
    autorun(cd_solvate)
    autorun(cd_genion)
    autorun(cd_grompp)
    autorun(cd_mdrun)
    autorun(cd_energy)
    #提示用户完成初始化 tobeadded，在底部框中给出生成文件链接供客户端下载,接下来修改mdp文件
    modify_mdp("ions.mdp")

def nvt_npt():    
    modify_mdp("nvt.mdp")
    modify_mdp("npt.mdp")
    autorun(cd_grompp_nvt)
    autorun(cd_mdrun_nvt)
    autorun(cd_energy_nvt)
    autorun(cd_grompp_npt)
    autorun(cd_mdrun_npt)
    autorun(cd_energy_npt)
    autorun(cd_energy_density)

    #提示用户完成分析 tobeadded，在底部框中给出生成文件链接供客户端下载，接下来修改其他mdp文件


def md():
    modify_mdp("md.mdp")
    autorun(cd_grompp_md)
    autorun(cd_mdrun_md)
    autorun(cd_trjconv)
    autorun(cd_rms)
    autorun(cd_rms_s)
    autorun(cd_gyrate)

    #提示完成md，点击跳转标签查看xvg等分析文件，在底部框中给出生成文件链接供客户端下载

def main():
    #根据网页读取的json修改各个命令行，每隔10秒自动执行指令，并输出运行的result，修改mdp文件，以及自动执行

if __name__ == '__main__':
    main()


