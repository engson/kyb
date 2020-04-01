<template>
  <div>
    <form-post
      v-bind.sync="form"
      @save-post="savePost"
      @clear-form="initForm"
      @delete-post="deletePost"
    />
    <list-post
      :posts="allPosts"
      @open-post="openPost"
    />
  </div>
</template>

<script>
// @ is an alias to /src
import FormPost from '@/components/FormPost.vue'
import ListPost from '@/components/ListPost.vue'
import api from '@/api'

export default {
  name: 'Form',
  components: {
    FormPost,
    ListPost
  },
  data () {
    return {
      form: null,
      allPosts: []
    }
  },
  methods: {
    initForm (insertForm) {
      this.form = {
        _id: '',
        post: '',
        comment: '',
        createdDateTime: '',
        editDateTime: '',
        ...insertForm
      }
    },
    async savePost () {
      const body = this.removeEmptyFromObj(this.form)
      const now = new Date()
      if (!body._id) {
        body.createdDateTime = now.toISOString()
        const response = await api.createPost(body)
        if (response.status === 200) {
          this.initForm(response.data)
          this.allPosts.push({ ...this.form })
        }
      } else {
        body.editDateTime = now.toISOString()
        const postId = body._id
        delete body._id
        const response = await api.editPost(postId, body)
        if (response.status === 200) {
          this.initForm(response.data)
          const idx = this.allPosts.findIndex(post => post._id === response.data._id)
          this.allPosts.splice(idx, 1, { ...this.form })
        }
      }
    },
    async openPost (postId) {
      const response = await api.getPost(postId)
      if (response.status === 200) {
        this.initForm(response.data)
      }
    },
    async deletePost () {
      const postId = this.form._id
      if (postId) {
        const response = await api.deletePost(postId)
        if (response.status === 204) {
          this.allPosts = this.allPosts.filter(function( post ) {
            return post._id !== postId
          })
          this.initForm()
        }
      }
    },
    removeEmptyFromObj (obj) {
      return Object.keys(obj)
        .filter(k => obj[k] != null && obj[k] != '') // Remove null and empty string.
        .reduce(
          (newObj, k) =>
            typeof obj[k] === "object"
              ? { ...newObj, [k]: this.removeEmpty(obj[k]) } // Recurse.
              : { ...newObj, [k]: obj[k] }, // Copy value.
          {}
        )
    }
  },
  async beforeCreate () {
    const response = await api.getAllPosts()
    if (response.status === 200 && response.data.length) {
      this.allPosts = response.data
    }
  },
  beforeMounted () {
    this.initForm()
  }
}
</script>
