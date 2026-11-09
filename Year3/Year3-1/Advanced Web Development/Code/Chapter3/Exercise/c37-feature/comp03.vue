<template>
  <el-card v-for="b in books" :key='b.title'>
    <template #header><span class="title">{{ b.title }}</span></template>
    <el-row>
      <el-col :span='6'><img :src="b.imageUrl" height="150"></el-col>
      <el-col :span='18'>
        <p>{{ b.synopsis }}</p>
        <a :href="b.moreInfo" target="_blank">[more info]</a>
      </el-col>
    </el-row>
  </el-card>

  <el-button type="primary" @click="swapBook">Swap the two book</el-button>
</template>

<script>
  import { ElCard, ElRow, ElCol, ElButton } from "element-plus";
  import 'element-plus/dist/index.css';

  export default {
    components: { ElCard, ElRow, ElCol, ElButton },
    data() {
      return {
        books: [
          {
            title: 'Principles of Gaming Technologies',
            imageUrl: 'https://www.mpu.edu.mo/cntfiles/upload/images/highlight/2021/013_ipm_grp_2021_p1.jpg',
            synopsis: `The academic book written by the Macao Polytechnic University’s (MPU) 
              Computing Programme titled "Principles of Gaming Technologies" was recently published 
              by McGraw Hill, a world-renowned publisher founded in 1888. Being the first academic book 
              in the field of gaming technology in Macao, it is of great significance to the internationalization 
              of Macao’s science and technology products, and contributes to the development of the 
              Guangdong-Hong Kong-Macao Greater Bay Area to become an International 
              Innovation & Technology Centre.`,
            moreInfo: 'https://www.mpu.edu.mo/en/highlights.php?hlight=45523'
          },
          {
            title: 'Global Gaming & Tourism Research',
            imageUrl: 'https://www.mpu.edu.mo/cntfiles/upload/images/highlight/2021/global_gaming_tourism_research_2021_vol_1.jpg',
            synopsis: `Macao Polytechnic University (MPU) has recently published the first issue of 
            Global Gaming & Tourism Research (Serial No.3) of 2021. This current issue of the Journal covers 
            academic papers on gaming and tourism with contributing authors from the United Kingdom, Mainland 
            China and Macao. The journal aims to promote the sustainable development of the gaming and 
            tourism industry and to provide support for science-based decision-making across the government 
            and gaming sectors. This academic journal seeks to serve as an exchange platform for gaming and 
            tourism research work.`,
            moreInfo: 'https://www.mpu.edu.mo/en/highlights.php?hlight=49205'
          }
        ]
      }

    },
    methods: {
      swapBook() {
        let first = this.books[0];
        this.books[0] = this.books[1];
        this.books[1] = first;
      }
    }
  }
</script>

<style scoped>
  @import url("//unpkg.com/element-plus/dist/index.css");

  .el-card {
    width: 80%;
    margin-bottom: 1em;
  }

  .el-card p {
    margin-top: 0;
    font-size: 90%;
  }

  .el-card a {
    font-size: 80%;
  }

  .el-card span.title {
    font-weight: bold
  }
</style>