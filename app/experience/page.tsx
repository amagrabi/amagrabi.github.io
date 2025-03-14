import styles from './page.module.css'

export default function Experience() {
  return (
    <div className={styles.experience}>
      <div className={styles.experienceEntry}>
        <div className={styles.date}>Dec 2021 - Sep 2024</div>
        <div className={styles.company}>BuildingMinds</div>
        <div className={styles.location}>Berlin</div>
        <div className={styles.position}>Head of AI & Data Science</div>
      </div>

      <div className={styles.experienceEntry}>
        <div className={styles.date}>Dec 2018 - Dec 2020</div>
        <div className={styles.company}>Commercetools</div>
        <div className={styles.location}>Berlin</div>
        <div className={styles.position}>Lead Data Scientist</div>
      </div>

      <div className={styles.experienceEntry}>
        <div className={styles.date}>Oct 2016 - Dec 2018</div>
        <div className={styles.company}>Commercetools</div>
        <div className={styles.location}>Berlin</div>
        <div className={styles.position}>Data Scientist</div>
      </div>
    </div>
  )
} 