<p align="center">
  <img src="docs/img/logo.svg" alt="Project Logo" width="200"/>
</p>

# 👾 Tetris Bugs: The Code Editor You Never Asked For

Built by **Grand Gardenias** for Python Discord's Summer CodeJam 2025. Challenge theme: **Wrong Tool for the Job** using **Python in the Browser** via [Pyscript](https://pyscript.net/).

---

## 🎯 The Concept

Instead of typing code like a normal human, you now have to **catch falling code blocks** and arrange them into working programs.

## 🎮 Game Modes (Choose Your Suffering)

### 1. 🏗️ Tetris Code Editor

- New File
- Export/Save
- Undo/Redo
- Run Code
- Terminal Output
- Code Falls from Sky

### 2. ⚡ CodeRush Mode

- 5-minute timer counting down
- Questions show up on the left
- Solve as many as you can before time’s up
- Your score = how many problems you solved before the end

### 3. 🗡️ Roguelike Mode

- We provide the CORRECT solution
- Arrange the blocks properly to "clear" lines like Tetris
- Wrong arrangements stack up
- Reach the top = GAME OVER

### 4. We could not finish the multiplayer mode, but it is documented in [docs/goals.md](docs/goals.md)  

## 🛠️ Tech Stack

- **PyScript**
- **TailwindCSS**

## 📦 Requirements

- Python 3.13+
- Node.js & npm

## ⚙️ Setup Instructions

1. Clone the repository:
    ```shell
    git clone https://github.com/zishankadri/tetris-bugs.git
    cd tetris-bugs
    ```
3. Start a local Server:
    ```shell
    cd frontend
    npm install
    npm run build
    python -m http.server
    ```

3. **Open Your Browser** to `http://localhost:8000`
4. 💡 For Contributors: Run `npm run dev` to auto-update Tailwind while you code.

## 🎉 Achievement Unlocked
**Congratulations! You now have the most unique answer to "What IDE do you use?"**

*"Oh, I use Tetris."*

## Video Presentation
[code-editor.webm](https://github.com/user-attachments/assets/cf059496-4f29-4d98-a95a-8969f91b333e)

<details>
    <summary>⚡ CodeRush Video Presentation </summary>
    https://drive.google.com/file/d/1t6_92z2R_ntOok2yyzjklHpKyxoKZl_g/view
</details>

<details>
    <summary>🗡️ Roguelike (BETA) Video Presentation </summary>

[roguelike.webm](https://github.com/user-attachments/assets/ffc35054-e3de-4e12-ac63-f1e3520f2ee8)
</details>

## 📸 Screenshots
<details>
    <summary>Preview Images 📸</summary>
    <img width="1314" height="655" alt="code-editor" src="https://github.com/user-attachments/assets/d3d61ead-39b7-44e8-b62f-207709f3b1b6" />
    <img width="1360" height="676" alt="code-editor" src="https://github.com/user-attachments/assets/b8d619c7-280e-4e5e-b9b6-c59bfa21ccf9" />
    <img width="1360" height="768" alt="code-rush" src="https://github.com/user-attachments/assets/6f6c9027-1017-43cc-95ef-c971d493ccb7" />
    <img width="1360" height="676" alt="roguelike" src="https://github.com/user-attachments/assets/4142aa8b-012b-4f29-85a0-8624e1ef33e5" />
    <img width="1311" height="655" alt="menu" src="https://github.com/user-attachments/assets/1220ca0c-c8a3-49f1-a50d-1bd76965e989" />

</details>

## 🎯 Wrong Tool for the Job

✅ Using Tetris as an IDE  
✅ Spatial reasoning for coding problems  

With some tweaks and backend, this could be a useful tool as a coding qualifier, as we doubt any LLM alone could pass this test.

## 🤝 Credits

(in order of contributed LOC):

<table>
  <tr>
    <th></th>
    <th>Name</th>
    <th>Contributions</th>
  </tr>
  <tr>
    <td><a href="https://github.com/zishankadri"><img src="https://github.com/zishankadri.png" alt="Luffy" width="64"></a></td>
    <td><a href="https://github.com/zishankadri">Luffy</a></td>
    <td>Lead developer, Project architecture, Ideation, Frontend</td>
  </tr>
  <tr>
    <td><a href="https://github.com/rxdiationx"><img src="https://github.com/rxdiationx.png" alt="rxdiationx" width="64"></a></td>
    <td><a href="https://github.com/rxdiationx">rxdiationx</a></td>
    <td>Base of CodeRush, sound effects/music, loading screen, Sourcing of problems</td>
  </tr>
  <tr>
    <td><a href="https://github.com/Sapient44"><img src="https://github.com/Sapient44.png" alt="Sapient44" width="64"></a></td>
    <td><a href="https://github.com/Sapient44">Sapient44</a></td>
    <td>Terminal and code execution, Modifications in roguelike mode, Sourcing of audio</td>
  </tr>
  <tr>
    <td><a href="https://github.com/Shivk123"><img src="https://github.com/Shivk123.png" alt="Shivk123" width="64"></a></td>
    <td><a href="https://github.com/Shivk123">Shivk123</a></td>
    <td>Meeting facilitation, Initial file structure, Set up Flask backend</td>
  </tr>
  <tr>
    <td><a href="https://github.com/mhaxanali"><img src="https://github.com/mhaxanali.png" alt="mhaxanali" width="64"></a></td>
    <td><a href="https://github.com/mhaxanali">mhaxanali</a></td>
    <td>timer logic, pause screen</td>
  </tr>
</table>
