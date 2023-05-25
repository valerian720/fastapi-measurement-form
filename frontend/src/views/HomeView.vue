<template>
  <div class="home">
    <MeasurementForm/>
  </div>
</template>

<script>
// @ is an alias to /src
import MeasurementForm from "@/components/MeasurementForm.vue";

export default {
  name: "HomeView",
  components: {
    MeasurementForm,
  },
};
</script>
