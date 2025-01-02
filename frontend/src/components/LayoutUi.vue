<template>
  <div class="container-fluid">
    <div class="row">
      <nav-bar></nav-bar>
      <div class="col-md-10 main">
        <slot name="main"></slot>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "LayoutUi"
}
</script>

<style>
.main {
  padding: 1rem;
  border-radius: 5px;
  border: 1px solid #dee2e6;
}

.table-container {
    overflow-x: auto;
    overflow-y: auto;
    border: 2px solid #f2f2f2;
    height: auto;
    border-radius: 5px;
}

th, td {
    border-bottom: 1px solid #ddd;
    text-align: center;
    //padding: 8px;
    color: darkslategray;
}

th {
    background-color: #f2f2f2;
    height: 30px;
    font-weight: 650;
}

td {
    height: 30px;
    font-size: 0.9rem;
}

table {
    width: 100%;
    border-bottom: 1px solid #ddd;
    border-collapse: collapse;
    border-radius: 5px;
}

.action-btn {
    background: linear-gradient(to left, #2C3646, #506582);
    color: white;
    padding: 5px 10px;
    border-radius: 5px;
    text-decoration: none;
}

.button {
    height: 50px;
    width: 50px;
    background: linear-gradient(to left, #2C3646, #506582);
    position: absolute;
    bottom: 30px;
    display: flex;
    justify-content: center;
    align-items: center;
    border-radius: 50%;
    left: 50%;
    right: 50%;
}

.button-text {
    text-decoration: none;
    color: white;
}


.verified-icon{
    height: 20px;
    width: 20px;
}

.content {
  margin-top: 2rem;
}
</style>