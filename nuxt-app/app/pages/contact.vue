<template>
  <div class="section-hero">
    <div class="container">
      <div class="section-hero-title">{{ contact.title }}</div>
      <div class="section-hero-subtitle">{{ contact.company }}</div>
    </div>
  </div>

  <div class="about-section" style="padding-bottom: 80px;">
    <div class="container footer-grid">
      <div class="footer-form">
        <div class="footer-title" style="color: #333;">{{ contact.form.title }}</div>
        <form @submit.prevent="onSubmit">
          <div class="footer-form-row">
            <label style="color: #333;">{{ contact.form.fields[0].label }}：</label>
            <input v-model="form.name" type="text" :placeholder="`请输入${contact.form.fields[0].label}`">
          </div>
          <div class="footer-form-row">
            <label style="color: #333;">{{ contact.form.fields[1].label }}：</label>
            <input v-model="form.phone" type="text" :placeholder="`请输入${contact.form.fields[1].label}`">
          </div>
          <div class="footer-form-row">
            <label style="color: #333;">{{ contact.form.fields[2].label }}：</label>
            <textarea v-model="form.message" :placeholder="`请输入${contact.form.fields[2].label}`"></textarea>
          </div>
          <button type="submit" class="footer-submit" style="background: #c1272d; color: #fff;">提交</button>
        </form>
      </div>

      <div class="footer-contact" style="color: #333;">
        <div class="footer-title" style="color: #333;">CONTACT US 联系我们</div>
        <p v-for="c in contact.contacts" :key="c.label">{{ c.label }}：{{ c.value }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import contact from '~/public/data/contact.json'

useHead({
  title: contact.title,
})

const form = reactive({
  name: '',
  phone: '',
  message: '',
})

function onSubmit() {
  alert('留言已提交，我们会尽快与您联系！')
  form.name = ''
  form.phone = ''
  form.message = ''
}
</script>
