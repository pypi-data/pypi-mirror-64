import solaredge_setapp
import solaredge_setapp.maintenance_pb2

import datetime


class Maintenance:
    
    def __init__(self, bytes=False):
        if bytes:
            return self.parse_protobuf(bytes)

    def parse_protobuf(self, bytes):
        
        # str name
        # int utf_offset
        # str ntp_server
        # int timestamp
        # list inverters {
            # str serial
            # dict isolation {int fault_location, int isolation, int alpha}
            # dict optimizers_status {int total, int online}
            # list optimizers {
                # str serial
                # bool online
                # float po_power
                # int po_voltage
                # int module_voltage
                # int module_current
                # int temperature 
                # int timestamp
            # }
        # }

        try:
            proto = solaredge_setapp.maintenance_pb2.Maintenance()
            proto.ParseFromString(bytes)
            
            parsed = {
                "system": str(proto.system.name),
                "utc_offset": int(proto.time.utc_offset),
                "ntp_server": str(proto.time.ntp_server),
                "timestamp": int(datetime.datetime.strptime(
                    "{year} {month} {day} {hour} {minutes} {seconds}".format(
                    year=proto.time.current_time.year,
                    month=proto.time.current_time.month,
                    day=proto.time.current_time.day,
                    hour=proto.time.current_time.hour,
                    minutes=proto.time.current_time.minutes,
                    seconds=proto.time.current_time.seconds
                ), "%Y %m %d %H %M %S").timestamp()),
                "afci": {
                    "enabled": proto.afci.enabled,
                    "manual_reconnect": proto.afci.manual_reconnect
                }
            }

            parsed["inverters"] = []

            for inverter in proto.diagnostics.inverters.primary, proto.diagnostics.inverters.left, proto.diagnostics.inverters.right:
                if inverter.serial:
                    parsed["inverters"].append({
                        "serial": str(inverter.serial),
                        "isolation": {
                            "fault_location": int(inverter.isolation.fault_location),
                            "isolation": int(inverter.isolation.r_iso.isolation),
                            "alpha": int(inverter.isolation.alpha.isolation)
                        },
                        "optimizers_status": {
                            "total": int(inverter.optimizers_status.total),
                            "online": int(inverter.optimizers_status.online)
                        },       
                        "optimizers": [{
                            "serial": str(po.serial),
                            "online": bool(po.online),
                            "po_power": float(po.po_power),
                            "po_voltage": int(po.po_voltage),
                            "module_voltage": int(po.module_voltage),
                            "module_current": int(po.module_current),
                            "temperature": int(po.temperature.value),
                            "timestamp": 0 if not bool(po.online) else int(datetime.datetime.strptime(
                                "{year} {month} {day} {hour} {minutes} {seconds}".format(
                                year=po.last_report.year,
                                month=po.last_report.month,
                                day=po.last_report.day,
                                hour=po.last_report.hour,
                                minutes=po.last_report.minutes,
                                seconds=po.last_report.seconds
                            ), "%Y %m %d %H %M %S").timestamp())
                        } for po in inverter.optimizer]
                })
        except AttributeError as e:
            print(f"AttributeError: {e}")

        return parsed
