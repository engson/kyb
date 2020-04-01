<template>
  <v-container>
    <v-row justify='center'>
      <v-col
        cols="6"
      >
        <v-text-field
          :value="_id"
          label="Post ID"
          placeholder=" "
          disabled
        />
      </v-col>
    </v-row>
    <v-row justify='center'>
      <v-col
        cols="6"
      >
        <v-textarea
          :value="post"
          label="Post"
          placeholder=" "
          @input="$emit('update:post', $event)"
        />
      </v-col>
    </v-row>
    <v-row justify='center'>
      <v-col
        cols="6"
      >
        <v-text-field
          :value="comment"
          label="Comment"
          placeholder=" "
          @input="$emit('update:comment', $event)"
        />
      </v-col>
    </v-row>
    <v-row justify='center'>
      <v-col cols="auto">
        <v-btn @click="$emit('save-post')">
          save
        </v-btn>
      </v-col>
      <v-col cols="auto">
        <v-btn @click="$emit('clear-form')">clear</v-btn>
      </v-col>
      <v-col cols="auto">
        <v-btn
          :disabled="!_id"
          @click="$emit('delete-post')"
        >
          delete
        </v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'FormPost',
  props: {
    _id: {
      type: String,
      default: ''
    },
    post: {
      type: String,
      default: ''
    },
    comment: {
      type: String,
      default: ''
    }
  }
}
</script>
