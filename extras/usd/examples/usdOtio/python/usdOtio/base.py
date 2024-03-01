
import json

class Base:

    yes = False
    verbose = False
    
    def __init__(self, otio_item = None):
        self.jsonData = {}
        if otio_item:
            self.from_json_string(otio_item.to_json_string())

    def from_json_string(self, s):
        self.jsonData = json.loads(s)
        
    def to_json_string(self):
        return json.dumps(self.jsonData)

    def to_usd(self, stage, usd_path):
        pass

    def _store_json_string(self, usd_path, usd_prim):
        #
        # Check if data is not empty
        #
        old_data = usd_prim.GetAttribute('jsonData').Get()
        if old_data and old_data != '':
            print(f'\n\nWarning jsonData for {usd_path} is not empty:')
            print(f'{old_data[:256]}...')
            self._continue_prompt()
            
        #
        # Attach the json data to the otio primitive
        #
        usd_prim.GetAttribute('jsonData').Set(self.to_json_string())
        
    def _continue_prompt(self):
        """
        Prompt user to continue or cancel.
        """
        if Base.yes:
            print("\nShall I continue (y/n)? ")
            print('y\n')
            return
        response = input("\nShall I continue (y/n)? ")
        if response.lower() == 'y':
            return
        elif response.lower() == 'n':
            print('Aborting...')
            exit(1)
        else:
            print("Invalid input. Please enter 'y' or 'n'.")
            self.continue_prompt()
