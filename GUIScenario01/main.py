#!/usr/bin/python
# coding: utf-8

from data.gui import GUI
import argparse


parser = argparse.ArgumentParser(description='Run the GUI')
parser.add_argument('-m', '--mode', type=str, help="Scenario mode like 'exploitation' or 'mitigation'", default='exploitation')
args = parser.parse_args()

interface = GUI(args.mode)
interface.run()
