<template>
  <v-container>
    <v-row>
      <v-col cols="12" align="center">
        <h2>This is a boilerplate app created with:</h2>
        <p>Frontend: Vue</p>
        <p>API: Flask</p>
        <p>Backend: MongoDB</p>
        <p>Deploy: Kubernetes</p>
        <h2>Ping the API to see if its up. There is also an example form page.</h2>
      </v-col>
      <v-col align="center">
        <v-btn mt-5 @click="pingApi">
          ping api
        </v-btn>
        <div>
          {{ data }}
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import api from '@/api'

export default {
  name: 'Home',
  data () {
    return {
      data: ''
    }
  },
  methods: {
    async pingApi () {
      try {
        const response = await api.ping()
        this.data = response.data
      } catch (err) {
        console.log(err)
        this.data = `An error occurred when trying to ping the API: ${err}`
      }
    }
  }
}
</script>
