<template>
  <v-container>
    <v-row align="center">
      <v-col>
        <v-data-table
          :headers="headers"
          :items="posts"
          @click:row="$emit('open-post', $event._id)"
        />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'ListPost',
  props: {
    posts: {
      type: Array,
      default: () => []
    }
  },
  data () {
    return {
      headers: [
        { text: 'ID',  value: '_id' },
        { text: 'Post',  value: 'post' },
        { text: 'Comment',  value: 'comment' },
        { text: 'Created',  value: 'createdDateTime' },
        { text: 'Edited',  value: 'editDateTime' },
      ]
    }
  }
}
</script>
