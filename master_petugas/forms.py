from django import forms

from . import models
from . import utils
import pandas as pd
from django.db.models import Q

from master_survey.models import SurveyModel

from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

class MasterPetugasForm(forms.ModelForm):
    
    class Meta:

        model = models.MasterPetugas
        fields = [
            'kode_petugas',
            'nama_petugas', 
            'nik',
            'npwp',
            'tgl_lahir',
            'pendidikan',
            'pekerjaan',
            'agama',
            'email',
            'no_telp',
            'alamat',
            'status'
        ]

        labels = {
            'kode_petugas': 'Kode Petugas',
            'nama_petugas': 'Nama Petugas', 
            'nik': 'NIK',
            'npwp': 'NPWP',
            'tgl_lahir': 'Tanggal Lahir',
            'pendidikan': 'Pendidikan',
            'pekerjaan': 'Pekerjaan',
            'agama': 'Agama',
            'email': 'Email',
            'no_telp': 'No Telp',
            'alamat': 'Alamat',
            'status': 'Status Petugas'
        }

        attrs_input = {
            'class' : 'form-control',
            'required': 'required',
            'placeholder': '...'
        }

        widgets = {
            'kode_petugas': forms.TextInput(
                attrs = attrs_input | {'autofocus': 'autofocus'}
            ),
            'nama_petugas': forms.TextInput(
                attrs = attrs_input | {'autofocus': 'autofocus'}
            ),
            'nik': forms.TextInput(
                attrs = attrs_input
            ),
            'npwp': forms.TextInput(
                attrs = attrs_input
            ),
            'tgl_lahir': forms.DateInput(
                attrs = attrs_input | {'type': 'date'}
            ),
            'pendidikan': forms.Select(
                attrs = attrs_input | {'class' : 'form-select'}
            ),
            'pekerjaan': forms.TextInput(
                attrs = attrs_input
            ),
            'agama': forms.Select(
                attrs = attrs_input | {'class' : 'form-select'}
            ),
            'email': forms.EmailInput(
                attrs = attrs_input
            ),
            'no_telp': forms.TextInput(
                attrs = attrs_input
            ),
            'alamat': forms.Textarea(
                attrs = attrs_input
            ),
            'status': forms.Select(
                attrs = attrs_input | {'class' : 'form-select'}
            ),
        }


class AlokasiForm(forms.ModelForm):
    
    class Meta:

        model = models.AlokasiPetugas
        fields = [
            'petugas', 
            'survey',
            'role'
        ]

        labels = {
            'petugas': 'Nama Petugas', 
            'survey': 'Nama Survei',
            'role': 'Jabatan'
        }

        attrs_input = {
            'class' : 'form-control',
            'required': 'required',
            'placeholder': '...'
        }

        widgets = {
            'petugas': forms.Select(
                attrs = attrs_input | {'class' : 'form-select', 'id': 'id_petugas_id'}
            ),
            'survey': forms.Select(
                attrs = attrs_input | {'class' : 'form-select', 'id' : 'id_survey_id'}
            ),
            'role': forms.Select(
                attrs = attrs_input | {'class' : 'form-select',  'id' : 'id_role_id'}
            )
        }


class RoleForm(forms.ModelForm):
    
    class Meta:

        model = models.RoleMitra
        fields = [
            'jabatan',
        ]

        labels = {
            'jabatan': 'Nama Jabatan'
        }

        attrs_input = {
            'class' : 'form-control',
            'required': 'required',
            'placeholder': '...'
        }

        widgets = {
            'jabatan': forms.TextInput(
                attrs = attrs_input
            ),
        }



class MasterPetugasFormUpload(forms.Form):
    import_file = forms.FileField(allow_empty_file=False,validators=[FileExtensionValidator(allowed_extensions=['xlsx'])], label="Import File Mitra", widget=forms.FileInput(
                              attrs={'class': "form-control"}))
    
    def clean(self):

        data = self.cleaned_data.get('import_file').read()

        df = pd.read_excel(data, skiprows=1, usecols='A:M', dtype='str')

        df.dropna(axis=0, how='all', inplace=True)

        headers = utils.get_verbose_fields(models.MasterPetugas, exclude_pk=True)
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
        
        
        # Validasi untuk non numerik value
        # Get option choices
        choices_status = dict(models.MasterPetugas._meta.get_field('status').choices)
        for idx, row in df['Status Mitra'].items():
            if row not in choices_status.values():
                base_errors.append(f'<b>Status Mitra</b> hanya dapat diisi {", ".join(choices_status.values())}. Harap periksa baris <b>{idx+1}</b>')
        df['Status Mitra'] = df['Status Mitra'].replace(list(choices_status.values()), list(choices_status.keys()))

        choices_pendidikan = dict(models.MasterPetugas._meta.get_field('pendidikan').choices)
        for idx, row in df['Pendidikan Terakhir'].items():
            if row not in choices_pendidikan.values():
                base_errors.append(f'<b>Pendidikan Terakhir</b> hanya dapat diisi {", ".join(choices_pendidikan.values())}. Harap periksa baris <b>{idx+1}</b>')
        df['Pendidikan Terakhir'] = df['Pendidikan Terakhir'].replace(list(choices_pendidikan.values()), list(choices_pendidikan.keys()))

        choices_agama = dict(models.MasterPetugas._meta.get_field('agama').choices)
        for idx, row in df['Agama'].items():
            if row not in choices_agama.values():
                base_errors.append(f'<b>Agama</b> hanya dapat diisi {", ".join(choices_agama.values())}. Harap periksa baris <b>{idx+1}</b>')
        df['Agama'] = df['Agama'].replace(list(choices_agama.values()), list(choices_agama.keys()))
        
        df['Tanggal Lahir'] = pd.to_datetime(df['Tanggal Lahir'], format='%d/%m/%Y')

        # Insert coloumn id to dataframe
        df.insert(loc=0, column='id', value='')

        # Convert verbose name as header of table to field_name
        field_names = utils.get_name_fields(models.MasterPetugas, exclude_pk = False)
        df.columns = field_names

        # Cek duplikasi Data pada master file    
        duplicated_petugas = df[df.duplicated('kode_petugas')].kode_petugas
        for idx, row in duplicated_petugas.items():
            base_errors.append(f'Duplikasi Kode Petugas: <b>{row}</b> ditemukan. Harap periksa baris <b>{idx+1}</b>')
        
        duplicated_nik = df[df.duplicated('nik')].nik
        for idx, row in duplicated_nik.items():
            base_errors.append(f'Duplikasi NIK: <b>{row}</b> ditemukan. Harap periksa baris <b>{idx+1}</b>')
        
        duplicated_npwp = df[df.duplicated('npwp')].npwp
        for idx, row in duplicated_npwp.items():
            base_errors.append(f'Duplikasi NPWP: <b>{row}</b> ditemukan. Harap periksa baris <b>{idx+1}</b>')
                
        duplicated_email = df[df.duplicated('email')].email
        for idx, row in duplicated_email.items():
            base_errors.append(f'Duplikasi Email: <b>{row}</b> ditemukan. Harap periksa baris <b>{idx+1}</b>')
        

        # Cek duplikasi Data pada Database
        db_petugas = models.MasterPetugas.objects.values_list('kode_petugas', 'nik', 'npwp', 'email')

        dt_petugas_sort = {
            'kode_petugas' : [],
            'nik' : [],
            'npwp' : [],
            'email' : [],
        }

        for dt in list(db_petugas):
            dt_petugas_sort['kode_petugas'].append(dt[0])
            dt_petugas_sort['nik'].append(dt[1])
            dt_petugas_sort['npwp'].append(dt[2])
            dt_petugas_sort['email'].append(dt[3])


        for idx, row in df['kode_petugas'].items():
            if row in dt_petugas_sort['kode_petugas']:
                base_errors.append(f'<b>Kode Petugas: [{row}]</b> telah tersedia pada database. Harap periksa baris <b>{idx+1}</b>')
      
        for idx, row in df['nik'].items():
            if row in dt_petugas_sort['nik']:
                base_errors.append(f'<b>NIK Petugas: [{row}]</b> telah tersedia pada database. Harap periksa baris <b>{idx+1}</b>')
      
        for idx, row in df['npwp'].items():
            if row in dt_petugas_sort['npwp']:
                base_errors.append(f'<b>NPWP Petugas: [{row}]</b> telah tersedia pada database. Harap periksa baris <b>{idx+1}</b>')
        
        for idx, row in df['email'].items():
            if row in dt_petugas_sort['email']:
                base_errors.append(f'<b>Email petugas: [{row}]</b> telah tersedia pada database. Harap periksa baris <b>{idx+1}</b>')
      
        if len(base_errors) > 0:
            self._errors['import_file'] = self.error_class(base_errors)
            return self._errors['import_file'] 


        for column in df.columns:


            if column in ['pendidikan', 'agama', 'status', models.MasterPetugas._meta.pk.name]:
                continue
            
            obj_field = models.MasterPetugas._meta.get_field(column)
            max_field = obj_field.max_length
            vname_field = obj_field.verbose_name
            
            index = df[df[column].astype(str).str.len() > max_field].index.tolist()
            rows = [idx+1 for idx in index]

            if len(rows) > 0:
                msg = f'Kesalahan pada kolom {vname_field}<ul>'
                for row in rows:
                    msg += f'<li>Kolom {vname_field} pada baris {row} memiliki panjang lebih dari {max_field} karakter</li>'
                msg += '</ul>'
                base_errors.append(msg)
       
    
        if len(base_errors) > 0:
            self._errors['import_file'] = self.error_class(base_errors)
            return self._errors['import_file'] 
        
        self.cleaned_data = df.to_dict()
        return self.cleaned_data


class AlokasiPetugasFormUpload(forms.Form):
    import_file = forms.FileField(allow_empty_file=False,validators=[FileExtensionValidator(allowed_extensions=['xlsx'])], label="Import Alokasi Petugas", widget=forms.FileInput(
                              attrs={'class': "form-control"}))
    
    def clean(self):

        def check_db(dataframe, col, data_list, base_errors):
            for idx, row in dataframe[col].items():

                id = [dt[1] for dt in data_list if dt[0] == row]
                if len(id) > 0 :
                    dataframe[col][idx] = id[0]
                else:
                    base_errors.append(f'<b>{col} [{row}]</b> tidak tersedia pada database mitra yang aktif. Harap periksa baris <b>{idx+1}</b>')

            return dataframe

        data = self.cleaned_data.get('import_file').read()

        df = pd.read_excel(data, skiprows=1, usecols='A:D', dtype='str')

        df.dropna(axis=0, how='all', inplace=True)
    

        headers = utils.get_verbose_fields(models.AlokasiPetugas, exclude_pk=True)
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
    
            
        # Validasi untuk non numerik value
        # Get option choices
        data_mitra = list(models.MasterPetugas.objects.filter(~Q(status = 1), ~Q(status = 3)).values_list('kode_petugas', 'id'))
        data_survei = list(SurveyModel.objects.values_list('nama', 'id'))
        data_role = list(models.RoleMitra.objects.values_list('jabatan', 'id'))

        check_db(df, 'Kode Petugas', data_mitra, base_errors)
        check_db(df, 'Survei/Sensus', data_survei, base_errors)  
        check_db(df, 'Jabatan Petugas', data_role, base_errors)  
    
        # Insert coloumn id to dataframe
        df.insert(loc=0, column='id', value='')

        # Convert verbose name as header of table to field_name
        field_names = utils.get_name_fields(models.AlokasiPetugas, exclude_pk = False)
        df.columns = field_names

        # Cek duplikasi Data pada master file    
        duplicated_petugas = df[df.duplicated()].petugas
        for idx, row in duplicated_petugas.items():
            base_errors.append(f'Duplikasi Kode Petugas: <b>{row}</b> dengan beban tugas yang sama ditemukan. Harap periksa baris <b>{idx+1}</b>')
      

        # Cek duplikasi Data pada database   
        for idx, row in df.iterrows():

            check_exist_data = models.AlokasiPetugas.objects.filter(petugas = row['petugas'], survey = row['survey'])

            if check_exist_data.exists():
                exist_data = check_exist_data.first()
                base_errors.append(f'Data Kode Petugas: <b>[{exist_data.petugas.kode_petugas}] {exist_data.petugas.nama_petugas} | {exist_data.survey.nama} *{exist_data.role.jabatan}</b> dengan beban tugas yang sama telah tersedia pada database. Harap periksa baris <b>{idx+1}</b>')

        if len(base_errors) > 0:
            self._errors['import_file'] = self.error_class(base_errors)
            return self._errors['import_file'] 

        
        self.cleaned_data = df.to_dict()
        return self.cleaned_data
    