<template>
  <footer>
    <div class="main-footer">
      <div class="container footer-grid">
        <div class="footer-form">
          <div class="footer-title">{{ contact.form.title }}</div>
          <ContactForm :fields="contact.form.fields" />
        </div>

        <div class="footer-contact">
          <div class="footer-title">CONTACT US 联系我们</div>
          <p v-for="c in contact.contacts" :key="c.label">{{ c.label }}：{{ c.value }}</p>
        </div>
      </div>
    </div>

    <div class="footer-bottom">
      <div class="container">
        {{ site.copyright }} | 备案号：
        <a :href="site.icpUrl" target="_blank" rel="noopener">{{ site.icp }}</a>
      </div>
    </div>
  </footer>
</template>

<script setup>
import site from '~/public/data/site.json'
import contact from '~/public/data/contact.json'
</script>
