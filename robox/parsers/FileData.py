class FileData:
    class Entry:
        def __init__(self, key, slot, value, units):
            self.value = value
            self.meta = {
                "name": key,
                "address": slot,
                "units": units,
            }

    def __init__(self):
        self.data = []

    def __str__(self):
        slots = sorted(list({entry.slot for entry in self.data}))
        keys = sorted(list({entry.key for entry in self.data}))

        output_array = {}

        for entry in self.data:
            if entry.slot not in output_array:
                output_array[entry.slot] = {}

            output_array[entry.slot][entry.key] = str(entry.value) + entry.units

        out = "Slot".ljust(10)
        for key in keys:
            out += key.rjust(25)
        out += "\n"

        for slot in slots:
            out += slot.ljust(10)
            for key in keys:
                if key in output_array[slot]:
                    out += output_array[slot][key].rjust(25)
                else:
                    out += " "*25
            out += "\n"

        return out

    def add_entry_with_slot_and_units(self, key, slot, value, units):
        self.data.append(self.Entry(key, slot, value, units))
