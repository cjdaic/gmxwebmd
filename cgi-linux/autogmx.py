#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import subprocess
import json
from time import sleep,time
import cgi
import os
sys.stdout.write("Content-Type: text/plain\n\n")

flag = ""
os.chdir("/var/www/html/usr")
def autorun(command):
     
    result = ""
    #command  = "bash -c '{}'".format(command)
    sys.stdout.write("Running: " + command + "\n")
    try:
        st = time()
        process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True)
        stdout = str(process.stdout.decode("utf-8"))
        stderr = str(process.stderr.decode("utf-8"))
        result += stdout
        result += stderr

        '''
        lines = result.split("\n")
        if "Richard Feynman" in lines[-1]:
            lines.pop()
            result = "\n".join(lines)
        if 'error' in result.lower():        
            sys.stdout.write("error in " + command +"\n")
            print(result)
            sys.exit(1)
        '''
        if command.split()[0] == "grep":
            log_file = log_dir + command.split()[0] + ".log"
        else:
            log_file = log_dir + command.split()[1] + ".log"
        with open(log_file, "w") as log:
            log.write(f"Command: {command}\n")
            log.write(result)
            log.write("\n")


    except subprocess.CalledProcessError as e:
        print("Operation Failed")
        print("error in " + command +"\n")
        print(e.output.decode("utf-8")+"\n")
        sys.exit(1)

    except TypeError as t:
        print("input error,please input again.")
        print("Operation Failed")


    sys.stdout.flush()
    sys.stdout.write("{} completed \n".format(command))
    end = time()
    sys.stdout.write('Running time: %s Seconds \n'%(end-st))
    sleep(1)

#打开/usr/usr.json文件
with open("usr.json","r",encoding='utf-8') as usr_conf:
    f = usr_conf.read()
    usr_data = json.loads(f)
#根据json文件读取用户名与各项参数，生成用户的文件目录，在里面生成gromacs所需的各项文件
###
#dir = usr_data.get("name")
#cd_mkdir = "mkdir " + dir
#cd_cd = "cd " +dir

#gromacs脚本
usr_dir = "/var/www/html/usr/"
log_dir = "log/"

cd_grep = "grep -v  HOH temp.pdb > temp_clean.pdb"
if usr_data.get("ignh"):
    ignh = " -ignh"
else :
    ignh = ""
cd_pdb2gmx = "gmx pdb2gmx -f  temp_clean.pdb -o  temp_processed.gro -ff " + usr_data.get("forcefield") + " -water " + usr_data.get("waterbox") + ignh + " -p topol.top"

if usr_data.get("ct"):
    ct = " -c"
else :
    ct = ""




cd_editconf = "gmx editconf -f  temp_processed.gro -o  temp_newbox.gro " + ct + " -d " + usr_data.get("dst") + " -bt " + usr_data.get("bt") + " > " + log_dir + "editconf.log"

cd_solvate = "gmx solvate -cp  temp_newbox.gro -cs " + usr_data.get("cs") + " -o  temp_solv.gro -p  topol.top > " + log_dir + "solvate.log"

cd_grompp = "gmx grompp -f  ions.mdp -c  temp_solv.gro -p  topol.top -o ions.tpr > " + log_dir + "grompp.log"

cd_grompp_em = "gmx grompp -f minim.mdp -c temp_solv_ions.gro -p topol.top -o em.tpr > " + log_dir + "grompp_em.log"

cd_genion = "gmx genion -s  ions.tpr -o  temp_solv_ions.gro -p  topol.top -pname NA -nname CL -neutral < genion.txt > " + log_dir + "genion.log"

cd_mdrun = "gmx mdrun -v -deffnm em  > " + log_dir + "mdrun.log"

cd_energy = "gmx energy -f  em.edr -o  usr_1.xvg < mdrun.txt > " + log_dir + "energy.log"

cd_grompp_nvt = "gmx grompp -f  nvt.mdp -c  em.gro -r  em.gro -p  topol.top -o  nvt.tpr > " + log_dir + "grompp_nvt.log"

cd_mdrun_nvt = "gmx mdrun -deffnm nvt > " + log_dir + "mdrun_nvt.log"

cd_energy_nvt = "gmx energy -f  nvt.edr -o  temperature.xvg < mdrun.txt > " + log_dir + "energy_nvt.log"

cd_grompp_npt = "gmx grompp -f  npt.mdp -c  nvt.gro -r  nvt.gro -t  nvt.cpt -p  topol.top -o  npt.tpr > " + log_dir + "grompp_npt.log"

cd_mdrun_npt = "gmx mdrun -deffnm npt " + log_dir + "mdrun_npt.log"

cd_energy_npt = "gmx energy -f  npt.edr -o  pressure.xvg  < mdrun.txt > " + log_dir + "energy_npt.log"

cd_energy_density = "gmx energy -f  npt.edr -o  density.xvg  < mdrun.txt> " + log_dir + "energy_density.log"

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
def mdrun():
    with open("mdrun.txt", "r+") as file:
        lines = file.readlines()
        lines[0] = usr_data.get("selections")+"\n"
        file.seek(0)
        file.writelines(lines)

