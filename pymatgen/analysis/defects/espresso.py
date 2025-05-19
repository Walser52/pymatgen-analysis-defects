
def fileread(func):
    def wrapper(cls, xml_file, *args, **kwargs):
        calc = PWxml(xml_file)
        struct = calc.get_computed_entry(entry_id = "")

        return func(cls, struct, *args, **kwargs)
    return wrapper
    

class QECalcTools:
    
    @classmethod
    @fileread
    def standardize_total_energy(cls, struct):
        e_bulk = struct.energy
        composition = struct.composition
        
        comp_dict = composition.as_data_dict()['unit_cell_composition']
        
        elements = comp_dict.keys()
        n_i = np.array(list(comp_dict.values()))
        u_i = np.array([get_element_formation_energy(elem) for elem in elements])
        
        std_form_energy = (e_bulk - np.sum(n_i*u_i))/np.sum(n_i)

        return std_form_energy
    
    @classmethod
    def standardized_computed_entry(cls, xml_file):
        """
        Return a computed entry with the standard formation enthalpy as total energy
        """
        calc = PWxml(xml_file)
        struct = calc.get_computed_entry(entry_id = "")

        d_ = {
           "energy": cls.standardize_total_energy(xml_file),
           "composition": struct.composition,
           "entry_id": "",
           "correction": 0, 
        }
        
        ent = ComputedEntry.from_dict(d_) 

        return ent

