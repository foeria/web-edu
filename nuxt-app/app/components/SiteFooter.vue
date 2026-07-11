<template>
  <footer>
    <div class="main-footer">
      <div class="container footer-grid">
        <div class="footer-form">
          <div class="footer-title">ONLINE MESSAGE 在线留言</div>
          <form @submit.prevent="onSubmit">
            <div class="footer-form-row">
              <label>家长姓名：</label>
              <input v-model="form.name" type="text" placeholder="请输入家长姓名">
            </div>
            <div class="footer-form-row">
              <label>联系电话：</label>
              <input v-model="form.phone" type="text" placeholder="请输入联系电话">
            </div>
            <div class="footer-form-row">
              <label>留言内容：</label>
              <textarea v-model="form.message" placeholder="请输入留言内容"></textarea>
            </div>
            <button type="submit" class="footer-submit">提交</button>
          </form>
        </div>

        <div class="footer-contact">
          <div class="footer-title">CONTACT US 联系我们</div>
          <p>联系人：林老师</p>
          <p>手机：{{ site.hotline }}</p>
          <p>微信：17615827726</p>
          <p>地址：山东省济南市</p>
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

const form = reactive({
  name: '',
  phone: '',
  message: '',
})

function onSubmit() {
  // Placeholder: real form submission will be wired to PHP backend later
  alert('留言已提交，我们会尽快与您联系！')
  form.name = ''
  form.phone = ''
  form.message = ''
}
</script>
