<template>
  <div>
    <SectionHero
      :title="contact.title"
      :subtitle="contact.company"
    />

    <div class="about-section contact-page">
      <div class="container footer-grid">
        <div class="footer-form">
          <div class="footer-title" style="color: #333;">{{ contact.form.title }}</div>
          <ContactForm :fields="contact.form.fields" :dark="false" />
        </div>

        <div class="footer-contact" style="color: #333;">
          <div class="footer-title" style="color: #333;">CONTACT US 联系我们</div>
          <p v-for="c in contact.contacts" :key="c.label">{{ c.label }}：{{ c.value }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import contact from '~/public/data/contact.json'

useHead({
  title: contact.title,
})
</script>
