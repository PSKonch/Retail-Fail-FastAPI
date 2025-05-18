import CategoriesList from "@/components/CategoriesList";

export default function Home() {
  return (
    <div style={{
      maxWidth: 900,
      margin: "0 auto",
      padding: "40px 10px"
    }}>
      <h1 style={{
        fontSize: "2.2rem",
        fontWeight: "bold",
        marginBottom: 28
      }}>Категории</h1>
      <CategoriesList />
    </div>
  );
}
