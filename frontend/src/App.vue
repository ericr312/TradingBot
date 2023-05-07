<template>
  <div>
    <h1>Trading Bot</h1>
    <form @submit.prevent="submitOrder">
      <label for="order">How many shares do you want to submit?</label>
      <input type="number" id="order" v-model="order" required>
      <button type="submit">Submit</button>
    </form>
    <div v-if="result">{{ result }}</div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      order: null,
      result: null,
    };
  },
  methods: {
    async submitOrder() {
      try {
        const response = await fetch('/submit_order', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ order: this.order }),
        });
        const data = await response.json();
        this.result = data.message;
      } catch (err) {
        console.error(err);
        this.result = 'An error occurred while submitting the order.';
      }
    },
  },
};
</script>
