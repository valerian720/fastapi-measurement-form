<template>
  <div>
    <MeasurmentReportTable/>
  </div>
</template>

<script>
// @ is an alias to /src
import MeasurmentReportTable from "@/components/MeasurmentReportTable.vue";

export default {
  name: "ReportView",
  components: {
    MeasurmentReportTable,
  },
};
</script>
