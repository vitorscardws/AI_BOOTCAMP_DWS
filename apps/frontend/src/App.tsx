import {
  BrowserRouter as Router,
  Routes,
  Route,
  NavLink,
} from "react-router-dom";
import TextToMongo from "./pages/TextToMongo";
import RagChat from "./pages/RagChat";
import "./Style/global.css";
import PptChat from "./pages/PptChat";

function App() {
  return (
    <Router>
      <div
        style={{
          position: "fixed",
          top: 0,
          width: "100%",
          backgroundColor: "#efefef",
          zIndex: 1000,
        }}
      >
        <nav style={{ padding: "1rem" }}>
          <NavLink
            to="/text-to-mongo"
            style={({ isActive }) => ({
              marginRight: "1rem",
              fontWeight: isActive ? "bold" : "normal",
            })}
          >
            Text-to-Mongo
          </NavLink>

          <NavLink
            to="/pdf-chat"
            style={({ isActive }) => ({
              marginRight: "1rem",
              fontWeight: isActive ? "bold" : "normal",
            })}
          >
            PDF Chat
          </NavLink>

          <NavLink
            to="/ppt-chat"
            style={({ isActive }) => ({
              marginRight: "1rem",
              fontWeight: isActive ? "bold" : "normal",
            })}
          >
            PPT Chat
          </NavLink>
        </nav>
      </div>

      <Routes>
        <Route path="/text-to-mongo" element={<TextToMongo />} />
        <Route path="/pdf-chat" element={<RagChat />} />
        <Route path="/ppt-chat" element={<PptChat />} />
      </Routes>
    </Router>
  );
}

export default App;
