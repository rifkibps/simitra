from django import forms
from . import models
from master_petugas import utils
import pandas as pd

from django.core.exceptions import ValidationError

from django.core.validators import FileExtensionValidator

class SurveiForm(forms.ModelForm):

    class Meta:
        model = models.SurveyModel

        fields = [
            'nama',
            'deskripsi',
            'tgl_mulai',
            'tgl_selesai',
            'status'
        ]

        labels = {
            'nama' : 'Nama Survei',
            'deskripsi' : 'Deskripsi Survei',
            'tgl_mulai' : 'Tanggal Mulai',
            'tgl_selesai': 'Tanggal Berakhir',
            'status': 'Status Survei'
        }

        attrs_input = {
            'class' : 'form-control',
            'required': 'required',
            'placeholder': '...'
        }

        widgets = {
            'nama': forms.TextInput(
                attrs = attrs_input
            ),
            'deskripsi':forms.Textarea(
                attrs = attrs_input | {'style':'height: 135px;'}
            ),
            'tgl_mulai': forms.DateInput(
                attrs = attrs_input | {'type': 'date'}
            ),
            'tgl_selesai': forms.DateInput(
                attrs = attrs_input | {'type': 'date'}
            ),
            'status': forms.Select(
                attrs = attrs_input |  {'class' : 'form-select'}
            )
        }

class SurveiFormUpload(forms.Form):
    import_file = forms.FileField(allow_empty_file=False,validators=[FileExtensionValidator(allowed_extensions=['xlsx'])], label="Import Kegiatan Pendataan", widget=forms.FileInput(
                              attrs={'class': "form-control"}))
    
    def clean(self):

        data = self.cleaned_data.get('import_file').read()

        df = pd.read_excel(data, skiprows=1, usecols='A:F', dtype='str')

        df.dropna(axis=0, how='all', inplace=True)


        headers = utils.get_verbose_fields(models.SurveyModel, exclude_pk=True)
        headers = ['No'] + headers
        if [str(x).lower() for x in df.columns] != [str(x).lower() for x in headers]:
            self._errors['import_file'] = self.error_class(['Format template tidak sesuai. Silahkan gunakan template yang telah disediakan.'])
            return self._errors['import_file']
            

        # Validate Non Values
        base_errors = []
        df.columns = headers
        df.drop(columns=df.columns[0], axis=1, inplace=True)

        df_null = df[df.isna().any(axis=1)]
        for idx, i in df_null.iterrows():
            null_cols = ', '.join(str(e).capitalize() for e in i[i.isna()].index)
            base_errors.append(f'Nilai kosong pada <b>Baris {idx+1}</b> ditemukan. Periksa kolom <b>({null_cols})</b>')
    

        choices_status = dict(models.SurveyModel._meta.get_field('status').choices)
        for idx, row in df['Status Survei'].items():
            if row not in choices_status.values():
                base_errors.append(f'<b>Status Survei</b> hanya dapat diisi {", ".join(choices_status.values())}. Harap periksa baris <b>{idx+1}</b>')
        df['Status Survei'] = df['Status Survei'].replace(list(choices_status.values()), list(choices_status.keys()))

        df['Tanggal Mulai'] = pd.to_datetime(df['Tanggal Mulai'], format='%d/%m/%Y')
        df['Tanggal Berakhir'] = pd.to_datetime(df['Tanggal Berakhir'], format='%d/%m/%Y')

        # Insert coloumn id to dataframe
        df.insert(loc=0, column='id', value='')

        # Convert verbose name as header of table to field_name
        field_names = utils.get_name_fields(models.SurveyModel, exclude_pk = False)
        df.columns = field_names
    
        if len(base_errors) > 0:
            self._errors['import_file'] = self.error_class(base_errors)
            return self._errors['import_file'] 
        
        self.cleaned_data = df.to_dict()
        return self.cleaned_data
    