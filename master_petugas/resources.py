from import_export import resources, widgets

from import_export.fields import Field
from .models import MasterPetugas, AlokasiPetugas, RoleMitra
from .helpers import ExcelDateWidget

class MasterPetugasResource(resources.ModelResource):

    kode_petugas = Field(attribute="kode_petugas", column_name="Kode Mitra")
    nama_petugas = Field(attribute="nama_petugas", column_name="Nama Mitra")
    nik = Field(attribute="nik", column_name="NIK")
    npwp = Field(attribute="npwp", column_name="NPWP")
    # tgl_lahir = Field(attribute="tgl_lahir", column_name="Tanggal Lahir", widget=ExcelDateWidget())
    pendidikan = Field(attribute="get_pendidikan_display", column_name="Pendidikan")
    pekerjaan = Field(attribute="pekerjaan", column_name="Pekerjaan")
    agama = Field(attribute="get_agama_display", column_name="Agama")
    email = Field(attribute="email", column_name="Email")
    no_telp = Field(attribute="no_telp", column_name="No. Telp")
    alamat = Field(attribute="alamat", column_name="Alamat")
    status = Field(attribute="get_status_display", column_name="Status Mitra")
    
    class Meta:
        model = MasterPetugas
        fields = (
            'id',
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
        )
        

class MasterAlokasiResource(resources.ModelResource):

    petugas__kode_petugas = Field(attribute="petugas__kode_petugas", column_name="Kode Mitra")
    petugas__nama_petugas = Field(attribute="petugas__nama_petugas", column_name="Nama Mitra")
    survey__nama = Field(attribute="survey__nama", column_name="Nama Kegiatan Survei/Sensus")
    role__jabatan = Field(attribute="role__jabatan", column_name="Jabatan")
   
    class Meta:
        model = AlokasiPetugas
    
        fields = (
            'petugas__kode_petugas',
            'petugas__nama_petugas',
            'survey__nama',
            'role__jabatan'
        )
        


class MasterRoleResource(resources.ModelResource):

    jabatan = Field(attribute="jabatan", column_name="Jabatan/Role Mitra")
    
    class Meta:
        model = RoleMitra
    
        fields = (
            'jabatan',
        )
        