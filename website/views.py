# import mysql.connector
import random
import gc
from .functions import No_Pending_exe
from .classes import memory, instruction, registers, Reservation_Stations, instructions_q, Reservation_Station
from .operations import issue, execute, write_back
from collections import deque

from flask import Blueprint, render_template, request, flash, jsonify, session, url_for
from flask_login import login_required, current_user

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':

        current_clock_cycle = 1
        branchInst_num = 0
        branchInst_taken = 0
        pc = request.form.get('start')
        lines = request.form.get('code')
        if pc =="" or lines =="":
            flash('PC or code should not be empty!', category='error')
        else:

            regsata = request.form.get('regs')
            data_mem = request.form.get('mem')

            queue = instructions_q(int(pc))
            global_pc = int(pc)
            lines = lines.split("\n")
            Load_store_queue = deque()

            for inst in lines:
                queue.insert(instruction(inst))

            Reservation_Stations1 = Reservation_Stations()
            regs = registers()
            memory1 = memory()
            if data_mem != "":
                mem_data = data_mem.split("\n")
                for m in mem_data:
                    prs = m.split(",")
                    print(prs)
                    ind = int(prs[0])
                    d = int(prs[1])
                    memory1.write(ind, d)
            if regsata != "":
                regs_data = regsata.split("\n")
                for r in regs_data:
                    prs = r.split(",")
                    ind = int(prs[0])
                    d = int(prs[1])
                    regs.write_register(ind, d)

            queue.print_insts()
            while True:
                # print("PC: " + str(global_pc))
                branch_taken = False
                is_issued = False
                complete = False
                if global_pc < len(queue):
                    instruction1 = queue.queue[global_pc]
                    # instruction.print()
                    RS_name = instruction1.type

                    free_station = Reservation_Stations1.search(RS_name)

                    if free_station is not None:
                        if not branch_taken:
                            if instruction1.type in ["BNE", "RET", "JAL"]:
                                branchInst_num += 1
                            issue(free_station, instruction1, regs, Load_store_queue, current_clock_cycle, global_pc)

                            is_issued = True

                else:
                    complete = True

                execute(Reservation_Stations1, regs, memory1, Load_store_queue, global_pc, current_clock_cycle)

                result = write_back(Reservation_Stations1, regs, memory1, Load_store_queue, global_pc, current_clock_cycle)
                if is_issued:
                    global_pc += 1
                if result is not None:
                    branch_taken = True
                    branchInst_taken += 1
                    global_pc = result

                if complete and No_Pending_exe(Reservation_Stations1) and not branch_taken:
                    break
                else:
                    current_clock_cycle += 1
            regs.print_registers()
            current_clock_cycle += 1
            ICP = 0
            for i in queue.queue:
                if i.write_start_time is not None:
                    ICP += 1
                if i.write_start_time is not None:
                    if i.type in ["RET", "JAL", "BNE"] and i.write_start_time< i.execute_end_time:
                        i.write_start_time = i.execute_end_time +1
                    else:
                        i.write_start_time += 1
                if i.write_start_time is None:
                    i.write_start_time = ""
                if i.issue_start_time is None:
                    i.issue_start_time = ""
                if i.execute_start_time is None:
                    i.execute_start_time = ""
                if i.execute_end_time is None:
                    i.execute_end_time = ""

            return render_template("exe.html", regs= regs, data=queue.queue, time=current_clock_cycle, ICP=ICP,
                                   branchInst_num=branchInst_num, branchInst_taken=branchInst_taken)
    return render_template("setup.html", user=current_user)
