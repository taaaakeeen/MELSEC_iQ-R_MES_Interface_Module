import csv
import os
import re
import json
import logging
import traceback
# ------------------------------------------------------------------------
logger = logging.getLogger(__name__)
FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(filename='mes_parser.log', level=logging.DEBUG, format=FORMAT, datefmt='%Y-%m-%d %H:%M:%S', encoding='utf-8')
# ------------------------------------------------------------------------
# INIT
ACCESS_FIELD_FILE = "ACCESS_FIELD.CSV"
ACCESS_TABLE_FILE = "ACCESS_TABLE.CSV"
DB_BUFFER_FILE = "DB_BUFFER.CSV"
DEVICE_TAG_COMPONENT_FILE = "DEVICE_TAG_COMPONENT.CSV"
DEVICE_TAG_FILE = "DEVICE_TAG.CSV"
DOT_MATRIX_LED_FILE = "DOT_MATRIX_LED.CSV"
GLOBAL_VARIABLE_FILE = "GLOBAL_VARIABLE.CSV"
JOB_FILE = "JOB.CSV"
LOCAL_VARIABLE_FILE = "LOCAL_VARIABLE.CSV"
NETWORK_FILE = "NETWORK.CSV"
PROJECT_FILE = "PROJECT.CSV"
SECURITY_FILE = "SECURITY.CSV"
TARGET_DEVICE_FILE = "TARGET_DEVICE.CSV"
TARGET_SERVER_FILE = "TARGET_SERVER.CSV"
USER_FILE = "USER.CSV"
# ------------------------------------------------------------------------
# JOB
JOB_NOTICE_FILE = "JOB_NOTICE.CSV"
TRIGGER_CONDITION_FILE = "TRIGGER_CONDITION.CSV"
# ------------------------------------------------------------------------
# ACTION
DB_ASSIGNMENT_FILE = "DB_ASSIGNMENT.CSV"
DB_COMMUNICATION_FILE = "DB_COMMUNICATION.CSV"
DB_NARROWING_DOWN_FILE = "DB_NARROWING_DOWN.CSV"
DB_SORTING_ORDER_FILE = "DB_SORTING_ORDER.CSV"
# ------------------------------------------------------------------------

def log_message(message):
    logger.debug(message)

def read_csv(file):
    data = []
    with open(file, 'r', newline='', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        for row in csv_reader:
            data.append(row)
    return data

def remove_brackets(text):
    return re.sub(r'\[[^\]]*\]', '', text)

def get_init_dir_list(dir_path):
    dir_path_list = []
    for obj_name in os.listdir(dir_path):
        obj_path = os.path.join(dir_path, obj_name)
        if os.path.isdir(obj_path):
            dir_path_list.append(obj_path)
    return dir_path_list

def merge_param(
        project_param, 
        network_param, 
        target_server_param, 
        target_device_param, 
        device_tag_param, 
        device_tag_component_param, 
        acccess_table_param, 
        acccess_field_param, 
        job_param,
        db_buffer_param,
        matrix_led_param,
        global_variable_param,
        local_variable_param,
        security_param,
        user_param
    ):
    param = {
        "PROJECT": project_param,
        "NETWORK": network_param,
        "TARGET_DEVICE": target_device_param,
        "DEVICE_TAG": device_tag_param,
        "DEVICE_TAG_COMPONENT": device_tag_component_param,
        "TARGET_SERVER": target_server_param,
        "ACCCESS_TABLE": acccess_table_param,
        "ACCCESS_FIELD": acccess_field_param,
        "JOB": job_param,
        "DB_BUFFER": db_buffer_param,
        "DOT_MATRIX_LED": matrix_led_param,
        "GLOBAL_VARIABLE": global_variable_param,
        "LOCAL_VARIABLE": local_variable_param,
        "SECURITY": security_param,
        "USER": user_param,
    }
    return param

def save_json(data, file):
    with open(file, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)

# str -> int
def convert_to_number(input_str):
    try:
        number = int(input_str)
        return number
    except ValueError:
        return input_str

# ------------------------------------------------------------------------
# INIT

# PROJECT.CSV
def get_project_param(init_dir_path):
    data = read_csv(os.path.join(init_dir_path, PROJECT_FILE))
    param = {
        "PROJECT_NAME": data[0][0],
        "COMMENT": data[0][1],
        "CSV_FORMAT_VERSION": convert_to_number(data[0][2])
    }
    return param

# NETWORK.CSV
def get_network_param(init_dir_path):
    data = read_csv(os.path.join(init_dir_path, NETWORK_FILE))
    param =  {
        "CH1": {
            "USE_CH1": data[0][0],
            "IP_ADDRESS": data[0][1],
            "SUBNET_MASK": data[0][2]
        },
        "CH2": {
            "USE_CH2": data[0][3],
            "IP_ADDRESS": data[0][4],
            "SUBNET_MASK": data[0][5]
        },
        "DEFAULT_GATEWAY": data[0][7],
        "HOST_NAME": data[0][8]
    }
    return param

# TARGET_SERVER.CSV
def get_target_server_param(init_dir_path):
    data = read_csv(os.path.join(init_dir_path, TARGET_SERVER_FILE))
    param = []
    for row in data:
        d = {
            "TARGET_SERVER_NUM": convert_to_number(row[0]), 
            "TARGET_SERVER_NAME": row[1],
            "COMMENT": row[2],
            "SERVER_TYPE": row[3],
            "ACCESS_TYPE": row[4],
            "IP_ADDRESS": row[5],
            "PORT_NUM": convert_to_number(row[6]),
            "COMMUNICATION_TIMEOUT": row[7],
            "DB_ACCESS_TIMEOUT": row[8],
            "DATA_SOURCE_NAME": row[9],
            "USER_NAME": row[10],
            "PASSWORD": row[11],
            "DATABASE_TYPE": row[12],
            "NOTIFY_ACCESS_ERROR": row[13],
            "NOTICE_DST": row[14]
        }
        param.append(d)
    return param

# TARGET_DEVICE.CSV
def get_target_device_param(init_dir_path):
    data = read_csv(os.path.join(init_dir_path, TARGET_DEVICE_FILE))
    param = []
    for row in data:
        d= {
            "TARGET_DEVICE_NUM": convert_to_number(row[0]),
            "TARGET_DEVICE_NAME": row[1],
            "COMMENT": row[2],
            "DEVICE_TYPE": row[3],
            "MULTIPLE_CPU": row[4],
            "SINGLE_NETWORK": row[5],
            "SOURCE_MODULE_TYPE": row[6],
            "SOURCE_ROUTE": row[7],
            "SOURCE_START_IO_NUM": convert_to_number(row[8]),
            "SOURCE_STATION_NUM": convert_to_number(row[9]),
            "ROUTED_IP_ADDRESS": row[10],
            "ROUTED_MODULE_TYPE": row[11],
            "ROUTED_NETWORK_NUM": convert_to_number(row[12]),
            "ROUTED_STATION_NUM": convert_to_number(row[13]),
            "TARGET_MODULE_TYPE": row[14],
            "TARGET_IP_ADDRESS": row[15],
            "TARGET_NETWORK_NUM": convert_to_number(row[16]),
            "TARGET_STATION_NUM": convert_to_number(row[17]),
            "DIFFERENT_NETWORK": row[18],
            "RELAY_MODULE_TYPE": row[19],
            "RELAY_START_IO_NUM": convert_to_number(row[20]),
            "CO-EX_NETWORK_NUM": convert_to_number(row[21]),
            "CO-EX_STATION_NUM": convert_to_number(row[22]),
            "GLOBAL_LABEL_SETTING": row[23],
            "GLOBAL_LABEL_PATH_SETTING": row[24]
        }
        param.append(d)
    return param

# DEVICE_TAG.CSV
def get_device_tag_param(init_dir_path):
    data = read_csv(os.path.join(init_dir_path, DEVICE_TAG_FILE))
    param = []
    for row in data:
        d= {
            "TAG_NUM": convert_to_number(row[0]),
            "TAG_NAME": row[1],
            "COMMENT": row[2],
            "PROTECT_DATA_WRITING": row[3],
            "ARRAY_TAG_SETTING": row[4],
            "ARRAY_SIZE": row[5],
            "ARRAY_TYPE": row[6],
            "SPECIFY_BLOCK_SIZE": row[7],
            "ARRAY_BLOCK_SIZE": row[8]
        }
        param.append(d)
    return param

# DEVICE_TAG_COMPONENT.CSV
def get_device_tag_component(init_dir_path):
    data = read_csv(os.path.join(init_dir_path, DEVICE_TAG_COMPONENT_FILE))
    param = []
    unique_values = set(row[0] for row in data)
    unique_values_list = list(unique_values)
    sorted_data = sorted(map(int, unique_values_list))
    for tag_num in sorted_data:
        tag_param = []
        for row in data:
            if tag_num == int(row[0]):
                d = {
                    "TAG_NUM": tag_num,
                    "COMPONENT_NUM": convert_to_number(row[1]),
                    "COMPONENT_NAME": row[2],
                    "TARGET_DEVICE_NUM": convert_to_number(row[3]),
                    "DEVICE_MEMORY": row[4],
                    "DATA_TYPE": row[5],
                    "LENGTH": convert_to_number(row[6]),
                    "GLOBAL_LABEL": row[7]
                }
                tag_param.append(d)
        param.append(tag_param)
    return param

# ACCESS_TABLE.CSV
def get_acccess_table_param(init_dir_path):
    data = read_csv(os.path.join(init_dir_path, ACCESS_TABLE_FILE))
    param = []
    for row in data:
        d = {
            "ACCESS_TABLE_NUM": convert_to_number(row[0]), 
            "ACCESS_TABLE_NAME": row[1],
            "COMMENT": row[2],
            "TARGET_SERVER_NUM": convert_to_number(row[3]),
            "TABLE_PROC_TYPE": row[4],
            "DB_TABLE_NAME": row[5]
        }
        param.append(d)
    return param

# ACCESS_FIELD.CSV
def get_acccess_field_param(init_dir_path):
    data = read_csv(os.path.join(init_dir_path, ACCESS_FIELD_FILE))
    param = []
    unique_values = set(row[0] for row in data)
    unique_values_list = list(unique_values)
    sorted_data = sorted(map(int, unique_values_list))
    for access_table_num in sorted_data:
        field_param = []
        for row in data:
            if access_table_num == int(row[0]):
                d = {
                    "ACCESS_TABLE_NUM": access_table_num,
                    "ACCESS_FIELD_NUM": convert_to_number(row[1]),
                    "ACCESS_FIELD_NAME": row[2],
                    "DB_FIELD_NAME": row[3],
                    "DATA_TYPE": remove_brackets(row[4]),
                    "PRECISION_HOLD": row[5],
                    "DEFAULT_VALUE_SETTING": row[6],
                    "DEFAULT_VALUE": row[7],
                    "DIRECTION": row[8]
                }
                field_param.append(d)
        param.append(field_param)
    return param

# JOB.CSV
def get_job_param(init_dir_path):
    data = read_csv(os.path.join(init_dir_path, JOB_FILE))
    param = []
    for row in data:
        d = {
            "JOB_NUM": convert_to_number(row[0]), 
            "JOB_NAME": row[1],
            "COMMENT": row[2],
            "JOB_CONFIGURATION": row[3],
            "PRE_ACTION_NUM": convert_to_number(row[4]),
            "POST_ACTION_NUM": convert_to_number(row[5]),
            "TRIGGER_CONFIGURATION": row[6],
            "TRIGGER_COMBINATION": row[7],
            "TRIGGER_BUFFERING": row[8],
            "ACCESS_TYPE": row[9],
            "ACCESS_INTERVAL": convert_to_number(row[10]),
            "ACCESS_INTERVAL_UNIT": row[11],
            "READING_TARGET": row[12],
            "PRE_FAIL_OPERATION": row[13],
            "MAIN_FAIL_OPERATION": row[14],
            "MAIN_ABORT_OPERATION": row[15],
            "DB_BUFFERING_SETTING": row[16],
            "DB_BUFFERING_OPERATION": row[17],
            "WORKING_HISTORY": row[18],
            "DETAILED_LOG": row[19],
            "INHIBIT_OUTPUT_DEVICE": row[20],
            "INHIBIT_OUTPUT_SERVER": row[21],
            "INHIBIT_JOB_EXECUTION": row[22]
        }
        param.append(d)
    return param

# ------------------------------------------------------------------------

# DB_BUFFER.CSV
def get_db_buffer_param(init_dir_path):
    data = read_csv(os.path.join(init_dir_path, DB_BUFFER_FILE))
    param = []
    for row in data:
        d = {
            "DB_BUFFER_NUM": convert_to_number(row[0]),
            "USE_DB_BUFFER": row[1],
            "DB_BUFFER_NAME": row[2],
            "DB_BUFFER_SIZE": row[3],
            "RESEND_AUTO": row[4],
            "OPERATION_RECOVERY": row[5],
            "RESEND_REQUEST": row[6],
            "CLEAR_REQUEST": row[7],
            "STATUS_NOTICE_DST": row[8],
            "NUM_NOTICE_DST": row[9],
            "FULL_NOTICE_DST": row[10],
            "USE_RATE_NOTICE_DST": row[11],
        }
        param.append(d)
    return param

# DOT_MATRIX_LED.CSV
def get_dot_matrix_led_param(init_dir_path):
    data = read_csv(os.path.join(init_dir_path, DOT_MATRIX_LED_FILE))
    param = []
    for row in data:
        d = {
            "DEFAULT_MODE": row[0],
            "SWITCH_FORCIBLY": row[1],
            "HIGHLIGHT_DISPLAY": row[2]
        }
        param.append(d)
    return param

# GLOBAL_VARIABLE.CSV
def get_global_variable_param(init_dir_path):
    data = read_csv(os.path.join(init_dir_path, GLOBAL_VARIABLE_FILE))
    param = []
    for row in data:
        d = {
            "VARIABLE_NUM": convert_to_number(row[0]),
            "VARIABLE_NAME": row[1],
            "COMMENT": row[2],
            "DATA_TYPE": row[3],
            "LENGTH": convert_to_number(row[4]),
        }
        param.append(d)
    return param

# LOCAL_VARIABLE.CSV
def get_local_variable_param(init_dir_path):
    data = read_csv(os.path.join(init_dir_path, LOCAL_VARIABLE_FILE))
    param = []
    for row in data:
        d = {
            "VARIABLE_NUM": convert_to_number(row[0]),
            "VARIABLE_NAME": row[1],
            "COMMENT": row[2],
            "DATA_TYPE": row[3],
            "LENGTH": convert_to_number(row[4]),
        }
        param.append(d)
    return param

# SECURITY.CSV
def get_security_param(init_dir_path):
    data = read_csv(os.path.join(init_dir_path, SECURITY_FILE))
    param = []
    for row in data:
        d = {
            "USE_USER_AUTH": row[0]
        }
        param.append(d)
    return param

# USER.CSV
def get_user_param(init_dir_path):
    data = read_csv(os.path.join(init_dir_path, USER_FILE))
    param = []
    for row in data:
        d = {
            "ACCOUNT_NUM": convert_to_number(row[0]),
            "USER_NAME": row[1],
            "PASSWORD": row[2]
        }
        param.append(d)
    return param

# ------------------------------------------------------------------------
# JOB

def get_job_dir_list(init_dir_path, job_param):
    l = []
    for param in job_param:
        job_num = param["JOB_NUM"]
        job_dir_name = f"JOB{str(job_num).zfill(2)}"
        job_dir_path = os.path.join(init_dir_path, job_dir_name)
        l.append(job_dir_path)
    return l

def add_trigger_condition_param(output_param, job_idx, trigger_condition_param):
    # print(output_param["JOB"][job_idx])
    new_param = output_param["JOB"][job_idx]
    new_param["TRIGGER_CONDITION"] = trigger_condition_param
    output_param["JOB"][job_idx] = new_param
    # print(output_param["JOB"][job_idx])
    return output_param

def add_job_notice_param(output_param, job_idx, job_notice_param):
    new_param = output_param["JOB"][job_idx]
    new_param["JOB_NOTICE"] = job_notice_param
    output_param["JOB"][job_idx] = new_param
    return output_param

# TRIGGER_CONDITION.CSV
def get_trigger_condition_param(job_dir_path):
    data = read_csv(os.path.join(job_dir_path, TRIGGER_CONDITION_FILE))
    param = []
    for row in data:
        d = {
            "TRIGGER_NUM": convert_to_number(row[0]), 
            "EVENT_CONDITION_TYPE": row[1],
            "DETAIL_TYPE": row[2],
            "MONITORING_TARGET": row[3],
            "CONDITION": row[4],
            "COMPARISON_TARGET": row[5],
            "MONTH": row[6],
            "DAY": row[7],
            "WEEK": row[8],
            "MON-SUN": row[9],
            "START_TIME": row[10],
            "END_TIME": row[11],
            "TIMER_INTERVAL": row[12],
            "TIME_INTERVAL": row[13],
            "TIME_INTERVAL_UNIT": row[14],
            "REFERENCE_TIME": row[15],
            "MESIF_MODULE_STARTUP": row[16],
            "MESIF_FUNC_RESTART": row[17],
            "CONTROL_CPU_STATUS": row[18],
            "REQUEST_SRC": row[19],
            "NOTICE_DST": row[20],
            "REQUEST_SRC2": row[21],
            "NOTICE_DST2": row[22]
        }
        param.append(d)
    return param

# JOB_NOTICE.CSV
def get_job_notice_param(job_dir_path):
    data = read_csv(os.path.join(job_dir_path, JOB_NOTICE_FILE))
    param = []
    for row in data:
        d = {
            "NOTICE_TYPE": row[0],
            "NOTICE_SETTING": row[1],
            "NOTICE_DST": row[2],
            "NOTICE_DATA": row[3]
        }
        param.append(d)
    return param

# ------------------------------------------------------------------------
# ACTION

def get_action_dir_list(job_dir_path):
    dir_path_list = []
    for obj_name in os.listdir(job_dir_path):
        obj_path = os.path.join(job_dir_path, obj_name)
        if os.path.isdir(obj_path):
            dir_path_list.append(obj_path)
    return dir_path_list
    
def add_action_param(output_param, job_idx, action_idx, db_assignment_param, db_communication_param, db_narrowing_down_param, db_sorting_order_param):
    new_param = output_param["JOB"][job_idx]
    d = {
        "ACTION_NUM": action_idx+1,
        "DB_COMMUNICATION": db_communication_param,
        "DB_NARROWING_DOWN": db_narrowing_down_param,
        "DB_SORTING_ORDER": db_sorting_order_param,
        "DB_ASSIGNMENT": db_assignment_param
    }
    new_param["ACTION"].append(d)
    output_param["JOB"][job_idx] = new_param
    return output_param

# DB_ASSIGNMENT.CSV
def get_db_assignment_param(action_dir_path):
    data = read_csv(os.path.join(action_dir_path, DB_ASSIGNMENT_FILE))
    param = []
    for row in data:
        d = {
            "ASSIGNMENT_NUM": convert_to_number(row[0]),
            "ACCESS_FIELD_NUM": convert_to_number(row[1]) ,
            "ASSIGNMENT_DATA": row[2]
        }
        param.append(d)
    return param

# DB_COMMUNICATION.CSV
def get_db_communication_param(action_dir_path):
    data = read_csv(os.path.join(action_dir_path, DB_COMMUNICATION_FILE))
    param = []
    for row in data:
        d = {
            "DB_COMMUNICATION_TYPE": row[0],
            "ACCESS_TABLE_NUM": convert_to_number(row[1]),
            "RECORD_NUM_NOTICE": row[2],
            "RECORD_NUM_DST": row[3],
            "SELECTED_RECORD_NUM_DST": row[4],
            "SET_MAX_RECORD_NUM": convert_to_number(row[5]),
            "MAX_RECORD_NUM": convert_to_number(row[6]),
            "M-SELECT_ZERO_CLEAR": row[7],
            "SET_DEFAULT_VALUE": row[8],
            "RETURN_VALUE_NOTICE": row[9],
            "RETURN_VALUE_DST": row[10],
            "NO_RECORD_OPERATION": row[11],
            "NO_RECORD_NOTICE": row[12],
            "NO_RECORD_NOTICE_DST": row[13],
            "NO_RECORD_NOTICE_DATA": row[14],
            "NO_RECORD_ZERO_CLEAR": row[15],
            "M-RECORDS_OPERATION": row[16],
            "M-RECORDS_NOTICE": row[17],
            "M-RECORDS_NOTICE_DST": row[18],
            "M-RECORDS_NOTICE_DATA": row[19],
            "OVERFLOW_OPERATION": row[20],
            "OVERFLOW_NOTICE": row[21],
            "OVERFLOW_NOTICE_DST": row[22],
            "OVERFLOW_NOTICE_DATA": row[23],
            "SELECT_FROM_FIRST": row[24],
            "INSERT_NEW_RECORD": row[25]
        }
        param.append(d)
    return param

# DB_NARROWING_DOWN.CSV
def get_db_narrowing_down_param(action_dir_path):
    data = read_csv(os.path.join(action_dir_path, DB_NARROWING_DOWN_FILE))
    param = []
    for row in data:
        d = {
            "NARROWING_DOWN_NUM": convert_to_number(row[0]),
            "COMBINATION": row[1],
            "ACCESS_FIELD_NUM": convert_to_number(row[2]),
            "CONDITION": row[3],
            "COMPARISON_TARGET": row[4]
        }
        param.append(d)
    return param

# DB_SORTING_ORDER.CSV
def get_db_sorting_order_param(action_dir_path):
    data = read_csv(os.path.join(action_dir_path, DB_SORTING_ORDER_FILE))
    param = []
    for row in data:
        d = {
            "SORTING_ORDER_NUM": convert_to_number(row[0]),
            "ACCESS_FIELD_NUM": convert_to_number(row[1]),
            "ORDER": row[2]
        }
        param.append(d)
    return param

# ------------------------------------------------------------------------

def add_job_param(init_dir_path, job_param, output_param):
    job_dir_list = get_job_dir_list(init_dir_path, job_param)
    for job_idx, job_dir_path in enumerate(job_dir_list):

        trigger_condition_param = get_trigger_condition_param(job_dir_path)
        # print(trigger_condition_param)

        job_notice_param = get_job_notice_param(job_dir_path)
        # print(job_notice_param)

        output_param = add_trigger_condition_param(output_param, job_idx, trigger_condition_param)
        output_param = add_job_notice_param(output_param, job_idx, job_notice_param)

        action_dir_list = get_action_dir_list(job_dir_path)

        output_param["JOB"][job_idx]["ACTION"] = []

        for action_idx, action_dir_path in enumerate(action_dir_list):

            db_assignment_param = get_db_assignment_param(action_dir_path)

            db_communication_param = get_db_communication_param(action_dir_path)

            db_narrowing_down_param = get_db_narrowing_down_param(action_dir_path)

            db_sorting_order_param = get_db_sorting_order_param(action_dir_path)

            output_param = add_action_param(output_param, job_idx, action_idx, db_assignment_param, db_communication_param, db_narrowing_down_param, db_sorting_order_param)

    return output_param 

# ------------------------------------------------------------------------

def main(init_dir_path):
    try:

        save_dir_path = OUTPUT_DIR
        print(init_dir_path)
        log_message(f"json変換開始: {init_dir_path}")

        project_param = get_project_param(init_dir_path)
        network_param = get_network_param(init_dir_path)
        target_server_param = get_target_server_param(init_dir_path)
        target_device_param = get_target_device_param(init_dir_path)
        device_tag_param = get_device_tag_param(init_dir_path)
        device_tag_component_param = get_device_tag_component(init_dir_path)
        acccess_table_param = get_acccess_table_param(init_dir_path)
        acccess_field_param = get_acccess_field_param(init_dir_path)
        job_param = get_job_param(init_dir_path)
        db_buffer_param = get_db_buffer_param(init_dir_path)
        matrix_led_param = get_dot_matrix_led_param(init_dir_path)
        global_variable_param = get_global_variable_param(init_dir_path)
        local_variable_param = get_local_variable_param(init_dir_path)
        security_param = get_security_param(init_dir_path)
        user_param = get_user_param(init_dir_path)
        output_param = merge_param(
            project_param, 
            network_param, 
            target_server_param, 
            target_device_param, 
            device_tag_param, 
            device_tag_component_param,
            acccess_table_param, 
            acccess_field_param, 
            job_param,
            db_buffer_param,
            matrix_led_param,
            global_variable_param,
            local_variable_param,
            security_param,
            user_param
        )
        output_param = add_job_param(init_dir_path, job_param, output_param)
        file_name = f'{os.path.basename(init_dir_path)}.json'
        save_file_path = os.path.join(save_dir_path, file_name)
        save_json(output_param, save_file_path)
        log_message(f"json変換完了: {save_file_path}")

    except Exception as e:
        logging.exception("An error occurred: %s", e)
        traceback_message = traceback.format_exc()
        print(traceback_message)

# 一括処理
def batch_processing(dir_path):
    init_dir_list = get_init_dir_list(dir_path)
    for init_dir_path in init_dir_list:
        main(init_dir_path)

if __name__ == '__main__':

    OUTPUT_DIR = os.path.join("dist", "output")
    
    # init_dir_path = os.path.join("data", "csv", "sample_01")
    # main(init_dir_path)

    dir_path = os.path.join("data", "csv")
    batch_processing(dir_path)


    