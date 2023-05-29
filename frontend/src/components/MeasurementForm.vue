<template>
  <div class="row">
    <div class="col col-lg-7 mx-auto">
      <div class="card text-start">
        <div class="card-body">
          <h4 class="card-title">Ввод замеров</h4>
          <div class="col m-1 p-1 help"
            title="Начните вводить данные / полностью окончите вводить данные для того что бы все пропуски сами заполнились">
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
                <option :value="department" v-for="(department, index) in departmentList" :key="index">
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
                    <th scope="col" rowspan="2" class="align-middle text-center">
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
                    <td scope="row" class="text-end">{{ rowIndex + 1 }}</td>
                    <td v-for="(cell, cellIndex) in row" v-bind:key="cellIndex">
                      <input v-model="cell.value" @change="changeCellTimestamp(rowIndex, cellIndex)" min="0.01" max="10"
                        step="0.01" type="number" class="form-control cell"
                        :title="createTMessage(cell.firstChanged, cell.lastChanged)" placeholder="x.xx">
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div class="mb-3">
              <label for="" class="form-label">Измерения выполнил: </label>
              <input type="text" class="form-control" name="responsible" aria-describedby="helpId" placeholder=""
                v-model="responsible" />
              <small id="helpId" class="form-text text-muted">Фамилия имя</small>
            </div>
            <div class="row">
              <button type="button" class="btn btn-outline-primary col-2 mx-auto" @click="sendData()"
              :disabled="!isEverythingInputed && canSave"
              >сохранить</button>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="alert alert-success " v-if="isSuccess" role="alert" @click="isSuccess = false">
      <h4 class="alert-heading">Сохранено</h4>
      <p>Введенные данные были успешно сохранены</p>
    </div>
    <div class="alert alert-danger"  v-if="isError" role="alert" @click="isError = false">
      <h4 class="alert-heading">Ошибка</h4>
      <p>Данные не были сохранены, попробуйте позднее или свяжитесь со специалистом</p>
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
      // responsible: "",
      responsible: "Иванов Василий",
      selectedDepartment: "1.1",
      //
      isEverythingInputed: false,
      canSave: true,
      //
      // cellTemplate: { value: "", firstChanged: null, lastChanged: null },
      cellTemplate: { value: "1", firstChanged: new Date(), lastChanged: new Date() },
      //
      // startedAtDateTime: null,
      // endedAtDateTime: null,
      startedAtDateTime: new Date(),
      endedAtDateTime: new Date(),

      departmentList: ["1.1", "1.2", "1.4", "1.5"],

      //
      msg: "",
      // 
      isSuccess: false,
      isError: false,
    };
  },
  methods: {
    hidePopups() {
      this.isSuccess = false;
      this.isError = false;
    },
    populateTable() {
      for (let i = 0; i < this.rowCount; i++) {
        let row = [];
        for (let j = 0; j < this.colCount; j++) {
          row.push({ ...this.cellTemplate });
        }
        this.table.push(row);
      }
    },
    changeCellTimestamp(i, j) {
      let cell = this.table[i][j];
      // 
      if (!cell.lastChanged) {
        cell.firstChanged = new Date();
      }
      cell.lastChanged = new Date();
      // 
      this.setTime();
      this.hidePopups();
    },
    // 
    setTime() {
      let count = this.countEmptyCells();
      if (count == this.rowCount * this.colCount - 1) {
        this.setStartTime();

      }
      if (count == 0) {
        this.setEndTime();
      }

    },
    setStartTime() {
      this.startedAtDateTime = new Date();
    },
    setEndTime() {
      this.endedAtDateTime = new Date();
      this.isEverythingInputed = true;
    },
    //
    sendData() {
      if (this.isEverythingInputed && this.canSave) {
        console.log("sending data");
        let postData = [];
        // convert data rom diiferent elements on form to objects 
        let template = {
          valve_number: -1,
          start_date: this.startedAtDateTime.toISOString(),
          end_date: this.endedAtDateTime.toISOString(),
          responsible: this.responsible,
          dripper_volume: 0,
          dripper_ec: 0,
          dripper_ph: 0,
          drain_volume: 0,
          drain_ec: 0,
          drain_ph: 0,
          mat_ec: 0,
          mat_ph: 0
        };
        for (let rowIndex = 0; rowIndex < this.rowCount; rowIndex++) {
          let curRow = this.table[rowIndex];
          let curObject = { ...template };
          curObject.valve_number = `${rowIndex+1}`;
          // pass data from row
          [ curObject.dripper_volume, 
          curObject.dripper_ec, 
          curObject.dripper_ph, 
          curObject.drain_volume, 
          curObject.drain_ec, 
          curObject.drain_ph, 
          curObject.mat_ec, 
          curObject.mat_ph ] = curRow.map((v) => v.value);
          // 
          postData.push(curObject);
        }
        // 
        axios
          .post("/v1/measurements/", postData)
          .then((res) => {
            console.log(res.data);
            this.isSuccess = true;
            this.canSave = false;
          })
          .catch((error) => {
            console.error(error);
            this.isError = true;
          });
      }

    },
    // 
    countEmptyCells() {
      return this.table.reduce((b, c) => (b + (c.reduce((b1, c1) => b1 + (c1.value == "" ? 1 : 0), 0))), 0);
    },
    createTMessage(initTime, changedTime) {
      return `добавлено в ${initTime ? initTime.toLocaleTimeString() : 'N/A'},изменено в ${changedTime ? changedTime.toLocaleTimeString() : 'N/A'}`;
    },
  },
  //
  mounted() {
    this.populateTable();
  },
};
</script>
<style>
.help {
  cursor: help;
}

td input:not(:placeholder-shown) {
  border-color: lightgreen;
}
</style>