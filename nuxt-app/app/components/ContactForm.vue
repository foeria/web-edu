<template>
  <form @submit.prevent="onSubmit">
    <div
      v-for="field in fields"
      :key="field.name"
      class="footer-form-row"
    >
      <label>{{ field.label }}：</label>
      <input
        v-if="field.name !== 'message'"
        v-model="form[field.name]"
        type="text"
        :placeholder="`请输入${field.label}`"
      >
      <textarea
        v-else
        v-model="form[field.name]"
        :placeholder="`请输入${field.label}`"
      />
    </div>
    <button type="submit" class="footer-submit">提交</button>
  </form>
</template>

<script setup>
const props = defineProps({
  fields: {
    type: Array,
    required: true,
  },
  dark: {
    type: Boolean,
    default: true,
  },
})

const form = reactive({
  name: '',
  phone: '',
  message: '',
})

function onSubmit() {
  // Placeholder: real form submission will be wired to PHP backend later
  alert('留言已提交，我们会尽快与您联系！')
  props.fields.forEach((field) => {
    form[field.name] = ''
  })
}
</script>
