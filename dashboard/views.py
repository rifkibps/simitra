import json
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import render

from django.db.models import Q
from master_petugas.models import MasterPetugas
from master_survey.models import SurveyModel
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from master_penilaian.models import KegiatanPenilaianModel, MasterNilaiPetugas
from django.http import JsonResponse, HttpResponse
from statistics import mean
from operator import itemgetter
from itertools import groupby

from django.urls import reverse_lazy

class MainDashboardClassView(LoginRequiredMixin, View):
    
    def get(self, request):

        context = {
            'title' : 'Dashboard',
            'mitra' : MasterPetugas.objects.all().count(),
            'mitra_block' : MasterPetugas.objects.filter(status =3).count(),
            'survey' : SurveyModel.objects.all().count(),
            'survey_finish' : SurveyModel.objects.filter(status = 2).count(),
            'penilaian' : KegiatanPenilaianModel.objects.all().count(),
            'penilaian_active' : KegiatanPenilaianModel.objects.filter(~Q(status = 1)).count(),
            'data_penilaian' : KegiatanPenilaianModel.objects.all(),
            'mitra_dinilai' : MasterNilaiPetugas.objects.values('petugas').distinct().count(),
            'nilai_mitra': MasterNilaiPetugas.objects.values('petugas', 'penilaian__kegiatan_penilaian').distinct().count(),
        }

        data = []

        db_nilai = MasterNilaiPetugas.objects.values('penilaian__indikator_penilaian__nama_indikator', 'nilai').order_by('penilaian__indikator_penilaian__nama_indikator')

        for idx, dt in enumerate(db_nilai):
  
            check_exist = [index for (index, d) in enumerate(data) if d["nama"] == dt['penilaian__indikator_penilaian__nama_indikator']]
            
            if len(check_exist) > 0:
                data[check_exist[0]]['data_series'].append(dt['nilai'])
                continue

            data.append({
                'nama' : dt['penilaian__indikator_penilaian__nama_indikator'],
                'rerata' : 0,
                'data_lain': '27%',
                'data_series': [dt['nilai'],],
            })

        data = data[:4]
        for idx, dt in enumerate(data):
            color = '#727cf5' if (idx+1) % 2 == 0 else '#0acf97'
            dt['rerata'] = round(float(mean(dt['data_series'])), 1)
            dt['min'] = round(float(min(dt['data_series'])), 1)
            dt['max'] = round(float(max(dt['data_series'])), 1)
            dt['color'] = color
            dt['data_series'] = dt['data_series'][-20:]
        
        context['summarize'] = data
        return render(request, 'dashboard/index.html', context)

class DashboardRankClassView(LoginRequiredMixin, View):

    def post(self, request):    
        data_wilayah = self._datatables(request)
        return HttpResponse(json.dumps(data_wilayah, cls=DjangoJSONEncoder), content_type='application/json')
		
    def _globalRank(self, request):
        data = MasterNilaiPetugas.objects.values('petugas__petugas__kode_petugas', 'petugas__petugas__nama_petugas', 'petugas__survey__nama', 'petugas__role__jabatan', 'penilaian__kegiatan_penilaian','penilaian__kegiatan_penilaian__nama_kegiatan', 'nilai')
        
        master_data = []
        
        for dt in data:
  
            check_exist = [index for (index, d) in enumerate(master_data) if d["kode_petugas"] == dt['petugas__petugas__kode_petugas']]
            
            if len(check_exist) > 0:

                check_exist_2 = [index for (index, d) in enumerate(master_data[check_exist[0]]['kegiatan_penilaian']) if d["id_kegiatan"] == dt['penilaian__kegiatan_penilaian']]
                
                if len(check_exist_2) > 0:
                    master_data[check_exist[0]]['kegiatan_penilaian'][check_exist_2[0]]['nilai'].append(dt['nilai'])
                else:
                    master_data[check_exist[0]]['kegiatan_penilaian'].append({
                        'id_kegiatan' : dt['penilaian__kegiatan_penilaian'],
                        'nama_kegiatan': dt['penilaian__kegiatan_penilaian__nama_kegiatan'],
                        'nilai' : [dt['nilai']]
                    })

                continue


            master_data.append({
                'kode_petugas': dt['petugas__petugas__kode_petugas'],
                'nama_petugas': dt['petugas__petugas__nama_petugas'],
                'rerata_final': 0,
                'ranking_final': 0,
                'kegiatan_penilaian' : [{'id_kegiatan': dt['penilaian__kegiatan_penilaian'] , 'nama_kegiatan': dt['penilaian__kegiatan_penilaian__nama_kegiatan'], 'nilai': [dt['nilai']]}]
            })

        for dt in master_data:
            
            mean_data = []
            for dt_kegiatan in dt['kegiatan_penilaian']:
                mean_data.append(round(mean(dt_kegiatan['nilai']), 2))
        
            dt['rerata_final'] = round(mean(mean_data), 2)

        data_sorted = sorted(master_data, key = itemgetter('rerata_final'), reverse=True)
        for idx, dt in enumerate(data_sorted):
            dt['ranking_final'] = idx+1

        return data_sorted


    def _datatables(self, request):


        datatables = request.POST
        
        # Get Draw
        draw = int(datatables.get('draw'))
        start = int(datatables.get('start'))
        length = int(datatables.get('length'))
        page_number = int(start / length + 1)

        search = datatables.get('search[value]')

        order_idx = int(datatables.get('order[0][column]')) # Default 1st index for
        order_dir = datatables.get('order[0][dir]') # Descending or Ascending
        order_col = 'columns[' + str(order_idx) + '][data]'
        order_col_name = datatables.get(order_col)

        if (order_dir == "desc"):
            order_col_name =  str('-' + order_col_name)


        data = MasterNilaiPetugas.objects
        if datatables.get('kegiatan_filter'):
            data = data.filter(penilaian__kegiatan_penilaian = datatables.get('kegiatan_filter'))

        data = data.values('petugas__petugas__id', 'petugas__petugas__kode_petugas', 'petugas__petugas__nama_petugas', 'petugas__survey__nama', 'petugas__role__jabatan', 'penilaian__kegiatan_penilaian__nama_kegiatan', 'nilai').exclude(Q(petugas=None)|Q(penilaian=None)|Q(nilai=None)|Q(catatan=None))

        records_total = data.count()
        records_filtered = records_total
    
        if search:
            data = MasterNilaiPetugas.objects

            if datatables.get('kegiatan_filter'):
                data = data.filter(penilaian__kegiatan_penilaian = datatables.get('kegiatan_filter'))

            data = data.filter(
                Q(petugas__petugas__kode_petugas__icontains=search)|
                Q(petugas__petugas__nama_petugas__icontains=search)|
                Q(petugas__role__jabatan__icontains=search)|
                Q(penilaian__kegiatan_penilaian__nama_kegiatan__icontains=search)
            ).values('petugas__petugas__id', 'petugas__petugas__kode_petugas', 'petugas__petugas__nama_petugas', 'petugas__survey__nama', 'petugas__role__jabatan', 'penilaian__kegiatan_penilaian__nama_kegiatan', 'nilai').exclude(Q(petugas=None)|Q(penilaian=None)|Q(nilai=None)|Q(catatan=None))
        
        if ('rerata' not in order_col_name) and ('ranking' not in order_col_name) and ('ranking_rerata' not in order_col_name) and ('ranking_final' not in order_col_name):
            data = data.order_by(order_col_name)

        data_df = []
        for dt in data:

            check_exist = [index for (index, d) in enumerate(data_df) if d["petugas__petugas__kode_petugas"] == dt['petugas__petugas__kode_petugas']]
            
            if len(check_exist) > 0:
                data_df[check_exist[0]]['rerata'].append(dt['nilai'])
                continue

            data_df.append({
                'petugas__petugas__id' : dt['petugas__petugas__id'],
                'petugas__petugas__kode_petugas': dt['petugas__petugas__kode_petugas'],
                'petugas__petugas__nama_petugas' : dt['petugas__petugas__nama_petugas'],
                'petugas__survey__nama': dt['petugas__survey__nama'],
                'petugas__role__jabatan' : dt['petugas__role__jabatan'],
                'penilaian__kegiatan_penilaian__nama_kegiatan': dt['penilaian__kegiatan_penilaian__nama_kegiatan'],
                'rerata' : [dt['nilai'],],
                'ranking': 0
            })

        for dt in data_df:
            dt['rerata'] = round(mean(dt['rerata']), 2)

        data_df = sorted(data_df, key = itemgetter('penilaian__kegiatan_penilaian__nama_kegiatan'))

        for key, value in groupby(data_df, key = itemgetter('penilaian__kegiatan_penilaian__nama_kegiatan')):

            dt_nilai = sorted(value, key=itemgetter('rerata'), reverse=True)
            for rank, k in enumerate(dt_nilai):
                k['ranking'] = rank+1


        global_ranking = self._globalRank(request)

        for dt in data_df:
            check_exist = [index for (index, d) in enumerate(global_ranking) if d["kode_petugas"] == dt['petugas__petugas__kode_petugas']]
            dt['rerata_final'] = global_ranking[check_exist[0]]['rerata_final']
            dt['ranking_final'] = global_ranking[check_exist[0]]['ranking_final']


        if 'rerata' in order_col_name:
            reverse = True if '-' in order_col_name else  False
            data_df = sorted(data_df, key=itemgetter('rerata'), reverse=reverse) 
        
        if 'ranking' in order_col_name:
            reverse = True if '-' in order_col_name else  False
            data_df = sorted(data_df, key=itemgetter('ranking'), reverse=reverse) 

        if 'rerata_final' in order_col_name:
            reverse = True if '-' in order_col_name else  False
            data_df = sorted(data_df, key=itemgetter('rerata_final'), reverse=reverse) 

        if 'ranking_final' in order_col_name:
            reverse = True if '-' in order_col_name else  False
            data_df = sorted(data_df, key=itemgetter('ranking_final'), reverse=reverse) 


        records_total = len(data_df)
        records_filtered = records_total

        # Conf Paginator    
        paginator = Paginator(data_df, length)

        try:
            object_list = paginator.page(page_number).object_list
        except PageNotAnInteger:
            object_list = paginator.page(1).object_list
        except EmptyPage:
            object_list = paginator.page(paginator.num_pages).object_list

        data = [
            {
                'petugas__petugas__nama_petugas': f'<a href="{reverse_lazy("master_petugas:mitra-view-detail", kwargs={"mitra_id": obj["petugas__petugas__id"]})}" class="text-body" target="_blank">{obj["petugas__petugas__nama_petugas"]}</a>',
                'petugas__survey__nama': obj['petugas__survey__nama'],
                'petugas__role__jabatan': obj['petugas__role__jabatan'],
                'penilaian__kegiatan_penilaian__nama_kegiatan': obj['penilaian__kegiatan_penilaian__nama_kegiatan'],
                'rerata': obj['rerata'],
                'ranking': obj['ranking'],
                'rerata_final': obj['rerata_final'],
                'ranking_final': obj['ranking_final'],
            } for obj in object_list
        ]
        
        return {
            'draw': draw,
            'recordsTotal': records_total,
            'recordsFiltered': records_filtered,
            'data': data,
        }

    def get(self, request):

        master_data = []

        data = MasterNilaiPetugas.objects.values('petugas__petugas__kode_petugas', 'petugas__petugas__nama_petugas', 'petugas__survey__nama', 'petugas__role__jabatan', 'penilaian__kegiatan_penilaian','penilaian__kegiatan_penilaian__nama_kegiatan', 'nilai')

        for dt in data:
  
            check_exist = [index for (index, d) in enumerate(master_data) if d["kode_petugas"] == dt['petugas__petugas__kode_petugas']]
            
            if len(check_exist) > 0:

                check_exist_2 = [index for (index, d) in enumerate(master_data[check_exist[0]]['kegiatan_penilaian']) if d["id_kegiatan"] == dt['penilaian__kegiatan_penilaian']]
                
                if len(check_exist_2) > 0:
                    master_data[check_exist[0]]['kegiatan_penilaian'][check_exist_2[0]]['nilai'].append(dt['nilai'])
                else:
                    master_data[check_exist[0]]['kegiatan_penilaian'].append({
                        'id_kegiatan' : dt['penilaian__kegiatan_penilaian'],
                        'nama_kegiatan': dt['penilaian__kegiatan_penilaian__nama_kegiatan'],
                        'nilai' : [dt['nilai']]
                    })

                continue


            master_data.append({
                'kode_petugas': dt['petugas__petugas__kode_petugas'],
                'nama_petugas': dt['petugas__petugas__nama_petugas'],
                'rerata_final': 0,
                'ranking_final': 0,
                'kegiatan_penilaian' : [{'id_kegiatan': dt['penilaian__kegiatan_penilaian'] , 'nama_kegiatan': dt['penilaian__kegiatan_penilaian__nama_kegiatan'], 'nilai': [dt['nilai']]}]
            })


        for dt in master_data:
            
            mean_data = []
            for dt_kegiatan in dt['kegiatan_penilaian']:
                mean_data.append(round(mean(dt_kegiatan['nilai']), 2))
            
            dt['rerata_final'] = round(mean(mean_data), 2)


        data_sorted = sorted(master_data, key = itemgetter('rerata_final'), reverse=True)
        for idx, dt in enumerate(data_sorted):
            dt['ranking_final'] = idx+1

        context = {
            'title' : 'Dashboard',
            'mitra' : MasterPetugas.objects.filter(~Q(status = 1)).count(),
            'survey' : SurveyModel.objects.filter(~Q(status = 1)).count(),
            'penilaian' : KegiatanPenilaianModel.objects.filter(~Q(status = 1)).count(),
            'data_penilaian' : KegiatanPenilaianModel.objects.all(),
        }
    
        return render(request, 'dashboard/index.html', context)


