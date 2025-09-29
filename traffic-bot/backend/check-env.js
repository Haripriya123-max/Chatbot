require('dotenv').config();

console.log("=== ENV TEST ===");
console.log("ORS_API_KEY =", process.env.ORS_API_KEY ? "Loaded ✅" : "Not Found ❌");
console.log("PORT =", process.env.PORT || "Not set");
