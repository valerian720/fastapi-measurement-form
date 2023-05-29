<template>
<div>
  <div class="table-responsive col col-lg-10 mx-auto">
    <div class="row m-1 p-1">Фильтры</div>
    <div class="row m-1 p-1">
      <div class="col">От 
        <div class="row m-1">
          <input type="datetime-local" v-model="timeStartFilter" @change="filterTable"/>
        </div>
      </div>
      <div class="col">До 
      <div class="row m-1">
        <input type="datetime-local" v-model="timeEndFilter" @change="filterTable"/>
      </div>
    </div>
      <div class="col">Отдел 
        <select class="form-select" aria-label="Отдел" v-model="departmentFilter" @change="filterTable">
        <option selected value="">не выбрано</option>
        <option :value="department" v-for="(department, index) in departmentList" :key="index">{{ department }}</option>
      </select>
    </div>
      <div class="col">Ответственный 
        <select class="form-select" aria-label="Отдел" v-model="responsibleFilter" @change="filterTable">
        <option selected value="">не выбрано</option>
        <option :value="responsible" v-for="(responsible, index) in responsibleList" :key="index">{{ responsible }}</option>
      </select>
    </div>
      <div class="col">№ клапана полива 
        <select class="form-select" aria-label="Отдел" v-model="valveNumberFilter" @change="filterTable">
        <option selected value="">не выбрано</option>
        <option :value="valveNumber" v-for="(valveNumber, index) in valveNumberList" :key="index">{{ valveNumber }}</option>
      </select>
    </div>
    </div>
    <table class="table table-striped
    table-hover	
    table-bordered
    align-middle"
    ref="table"
    >
      <thead class="table-light">
        <tr>
          <th rowspan="2">#</th>
          <th rowspan="2">Дата и время</th>
          <th rowspan="2" class="d-none">Дата и время начала</th>
          <th rowspan="2" class="d-none">Дата и время окончания</th>
          <th rowspan="2">Отдел</th>
          <th rowspan="2">ответственный</th>
          <th scope="col" rowspan="2">
            № клапана полива
          </th>
          <th scope="col" colspan="3">Капельница</th>
          <th scope="col" colspan="3">Дренаж</th>
          <th scope="col" colspan="2">Мат</th>
        </tr>
        <tr>
          <th scope="col">Объем</th>
          <th scope="col">ЕС</th>
          <th scope="col">рН</th>
          <th scope="col">Объем</th>
          <th scope="col">ЕС</th>
          <th scope="col">рН</th>
          <th scope="col">ЕС</th>
          <th scope="col">рН</th>
        </tr>
        </thead>
        <tbody class="table-group-divider">
          <tr class="" v-for="(row, index) in tableFiltered" :key="index">
            <td scope="row">{{ index + 1 }}</td>
            <td>
              {{new Date(row.start_date).toLocaleDateString()}}
              ({{new Date(row.start_date).toLocaleTimeString()}}
              -  
              {{new Date(row.end_date).toLocaleTimeString()}})
            </td>
            <td class="d-none">{{new Date(row.start_date).toLocaleString()}}</td>
            <td class="d-none">{{new Date(row.end_date).toLocaleString()}}</td>
            <td>{{row.department}}</td>
            <td>{{row.responsible}}</td>
            <td>{{row.valve_number}}</td>
            <td>{{row.dripper_volume}}</td>
            <td>{{row.dripper_ec}}</td>
            <td>{{row.dripper_ph}}</td>
            <td>{{row.drain_volume}}</td>
            <td>{{row.drain_ec}}</td>
            <td>{{row.drain_ph}}</td>
            <td>{{row.mat_ec}}</td>
            <td>{{row.mat_ph}}</td>
          </tr>
        </tbody>
        <tfoot>
          
        </tfoot>
    </table>
  </div>
  <div class="row">
    <button type="button" class="btn btn-primary col-6 col-lg-2 mx-auto" @click="downloadData()">Скачать</button>
  </div>
</div>
</template>

<script lang="js">
import axios from "axios";

export default {
  name: "MeasurmentReportTable",
  data() {
    return {
      table: [],
      tableFiltered: [],
      // 
      departmentList: [],
      valveNumberList: [],
      responsibleList: [],
      // 
      timeStartFilter: null,
      timeEndFilter: null,
      departmentFilter: "",
      responsibleFilter: "",
      valveNumberFilter: "",
    };
  },
  methods: {
    getTableCollumnShortList(key) {
      return [...new Set(this.table.map((v) => v[key]))];
    },
    downloadData() {
      let htmls = "";
      let uri = 'data:application/vnd.ms-excel;base64,';
      let template = '<html xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:x="urn:schemas-microsoft-com:office:excel" xmlns="http://www.w3.org/TR/REC-html40"><head><!--[if gte mso 9]><xml><x:ExcelWorkbook><x:ExcelWorksheets><x:ExcelWorksheet><x:Name>{worksheet}</x:Name><x:WorksheetOptions><x:DisplayGridlines/></x:WorksheetOptions></x:ExcelWorksheet></x:ExcelWorksheets></x:ExcelWorkbook></xml><![endif]--></head><body><table>{table}</table></body></html>'; 
      let base64 = function(s) {
          return window.btoa(unescape(encodeURIComponent(s)))
      };

      let format = function(s, c) {
          return s.replace(/{(\w+)}/g, function(m, p) {
              return c[p];
          })
      };

      htmls = this.$refs.table.innerHTML;

      let ctx = {
          worksheet : 'Отчет',
          table : htmls
      }

      let link = document.createElement("a");
      link.download = "report.xls";
      link.href = uri + base64(format(template, ctx));
      link.click();
    },
    filterTable() {
      let timeStart = new Date(this.timeStartFilter);
      let timeEnd = new Date(this.timeEndFilter);

      let ret = [...this.table]; // copy list of links to rows of table
      // 
      if (this.timeStartFilter) {
        ret = ret.filter((v) => new Date(v.start_date) >= timeStart);
      }
      if (this.timeEndFilter) {
        ret = ret.filter((v) => new Date(v.end_date) <= timeEnd);
      }
      if (this.departmentFilter) {
        ret = ret.filter((v) => v.department == this.departmentFilter);
      }
      if (this.responsibleFilter) {
        ret = ret.filter((v) => v.responsible == this.responsibleFilter);
      }
      if (this.valveNumberFilter) {
        ret = ret.filter((v) => v.valve_number == this.valveNumberFilter);
      }

      this.tableFiltered = ret;
    },
    calculateFilters() {
      this.departmentList = this.getTableCollumnShortList("department");
      this.valveNumberList = this.getTableCollumnShortList("valve_number");
      this.responsibleList = this.getTableCollumnShortList("responsible");
    },
    getData() {
      console.log("getting data");
      axios
        .get("/v1/measurements/")
        .then((res) => {
          this.table = res.data;
          this.calculateFilters();
          this.filterTable();
        })
        .catch((error) => {
          console.error(error);
        });
    },
    // 
  },
  //
  mounted() {
    this.getData();
  },
};
</script>
<style>

</style>