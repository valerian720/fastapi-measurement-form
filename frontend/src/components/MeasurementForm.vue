<template>
  <div class="row">
    <div class="col col-lg-7 mx-auto">
      <div class="card text-start">
        <div class="card-body">
          <h4 class="card-title">Ввод замеров</h4>
          <div class="col m-1 p-1 help" title="Начните вводить данные / полностью окончите вводить данные для того что бы все пропуски сами заполнились">
            Дата измерений:
            <u v-if="startedAtDateTime">{{
              startedAtDateTime.toLocaleDateString()
            }}</u>
            <u v-else>____</u> Время замеров: от
            <u v-if="startedAtDateTime">{{
              startedAtDateTime.toLocaleTimeString()
            }}</u>
            <u v-else>____</u>
            до
            <u v-if="endedAtDateTime">{{
              endedAtDateTime.toLocaleTimeString()
            }}</u>
            <u v-else>____</u>
          </div>
          <div class="row m-1 p-1">
            <div class="col-2 m-1 p-1">Отделение:</div>
            <div class="col-2">
              <select class="form-select" v-model="selectedDepartment" aria-label="выберите отдел">
                <option
                  :value="department"
                  v-for="(department, index) in departmentList"
                  :key="index"
                >
                  {{ department }}
                </option>
              </select>
            </div>
          </div>
          <div class="row">
            <div class="table-responsive">
              <table class="table table-striped table-bordered">
                <thead class="table-light">
                  <tr>
                    <th
                      scope="col"
                      rowspan="2"
                      class="align-middle text-center"
                    >
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
                <tbody>
                  <tr v-for="(row, rowIndex) in table" v-bind:key="rowIndex">
                    <td scope="row" class="text-end">{{ rowIndex+1 }}</td>
                    <td v-for="(cell, cellIndex) in row" v-bind:key="cellIndex">
                          <input v-model="cell.value" @change="changeCellTimestamp(rowIndex, cellIndex)"
                           min="0.01" 
                           max="10" 
                           step="0.01" 
                           type="number" 
                           class="form-control cell" 
                           :title="createTMessage(cell.firstChanged, cell.lastChanged)"
                           placeholder="x.xx">
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div class="mb-3">
              <label for="" class="form-label">Измерения выполнил: </label>
              <input
                type="text"
                class="form-control"
                name="responsible"
                aria-describedby="helpId"
                placeholder=""
                v-model="responsible"
              />
              <small id="helpId" class="form-text text-muted"
                >Фамилия имя</small
              >
            </div>
            <div class="row">
              <button type="button" class="btn btn-outline-primary col-2 mx-auto">сохранить</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "MeasurementForm",
  data() {
    return {
      table: [],
      rowCount: 6,
      colCount: 8,
      // 
      responsible: "",
      selectedDepartment: "1.1",
      //
      isEverythingInputed: false,
      //
      cellTemplate: { value: "", firstChanged: null, lastChanged: null },
      //
      startedAtDateTime: null,
      endedAtDateTime: null,
      departmentList: ["1.1", "1.2", "1.4", "1.5"],

      //
      msg: "",
    };
  },
  methods: {
    populateTable() {
      for (let i = 0; i < this.rowCount; i++) {
        let row = [];
        for (let j = 0; j < this.colCount; j++) {
          row.push({...this.cellTemplate});
        }   
        this.table.push(row);    
      }
      console.log(this.table);
    },
    changeCellTimestamp(i, j) {
      let cell = this.table[i][j];
      // 
      if (! cell.lastChanged) {
        cell.firstChanged = new Date();
      }
      cell.lastChanged = new Date();
      // 
      this.setTime();
    },
    // 
    setTime() {
      let count = this.countEmptyCells();
      console.log(count, this.rowCount * this.colCount);
      if (count == this.rowCount * this.colCount-1) {
        this.setStartTime();
        
      }
      if (count == 0) {
        this.setEndTime();
      }

    },
    setStartTime() {
      console.log("setStartTime");
      this.startedAtDateTime = new Date();
    },
    setEndTime() {
      console.log("setEndTime");
      this.endedAtDateTime = new Date();
      this.isEverythingInputed = true;
    },
    //
    sendData() {
      if (this.isEverythingInputed) {
        axios
          .post("/")
          .then((res) => {
            this.msg = res.data;
          })
          .catch((error) => {
            console.error(error);
          });
      }

    },
    // 
    countEmptyCells() {
      return this.table.reduce((b, c)=> (b + (c.reduce((b1, c1)=>b1 + (c1.value == "" ? 1:0),0))), 0);
    },
    createTMessage(initTime, changedTime) {
      return `добавлено в ${initTime? initTime.toLocaleTimeString(): 'N/A'},изменено в ${changedTime? changedTime.toLocaleTimeString(): 'N/A'}`;
    },
  },
  //
  mounted() {
    this.populateTable();
  },
};
</script>
<style>
.help {cursor: help;}

td input:not(:placeholder-shown) {
  border-color: lightgreen;
}
</style>