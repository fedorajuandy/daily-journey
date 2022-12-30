/* 
Sorting table

https://www.w3schools.com/howto/howto_js_sort_table.asp
*/
function sortTable(n) {
  let table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0, j
  table = document.getElementById("table-item")
  switching = true
  dir = "asc"

  while (switching) {
    switching = false
    rows = table.rows
    let rowsLenMin1 = rows.length - 1
    let colsLenMin1 = table.rows[0].cells.length - 1

    for (i = 1; i < rowsLenMin1; i++) {
      shouldSwitch = false
      x = rows[i].getElementsByTagName("TD")[n]
      y = rows[i + 1].getElementsByTagName("TD")[n]

      if (dir == "asc") {
        for (j = 0; j < colsLenMin1; j ++) {
          if (j === n) {
            document.getElementById("th" + j).innerHTML =
              `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-caret-up-fill" viewBox="0 0 16 16">
                <path d="m7.247 4.86-4.796 5.481c-.566.647-.106 1.659.753 1.659h9.592a1 1 0 0 0 .753-1.659l-4.796-5.48a1 1 0 0 0-1.506 0z"/>
              </svg>`
          }
          else {
            document.getElementById("th" + j).innerHTML = ''
          }
        }

        if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
          shouldSwitch = true
          break
        }
      } else if (dir == "desc") {
        for (j = 0; j < colsLenMin1; j ++) {
          if (j === n) {
            document.getElementById("th" + j).innerHTML =
            `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-caret-down-fill" viewBox="0 0 16 16">
              <path d="M7.247 11.14 2.451 5.658C1.885 5.013 2.345 4 3.204 4h9.592a1 1 0 0 1 .753 1.659l-4.796 5.48a1 1 0 0 1-1.506 0z"/>
            </svg>`
          }
          else {
            document.getElementById("th" + j).innerHTML = ''
          }
        }

        if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
          shouldSwitch = true
          break
        }
      }
    }

    if (shouldSwitch) {
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i])
      switching = true
      switchcount ++
    } else {
      if (switchcount == 0 && dir == "asc") {
        dir = "desc"
        switching = true
      }
    }
  }
}

function sortNumber(n) {
  let table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0, j
  table = document.getElementById("table-item")
  switching = true
  dir = "asc"

  while (switching) {
    switching = false
    rows = table.rows
    let colsLenMin1 = table.rows[0].cells.length - 1

    for (i = 1; i < (rows.length - 1); i++) {
      shouldSwitch = false
      x = rows[i].getElementsByTagName("TD")[n]
      y = rows[i + 1].getElementsByTagName("TD")[n]
      let isiX = Number((x.innerHTML).replace(/[^0-9]/g,''))
      let isiY = Number((y.innerHTML).replace(/[^0-9]/g,''))

      if (dir == "asc") {
        for (j = 0; j < colsLenMin1; j ++) {
          if (j === n) {
            document.getElementById("th" + j).innerHTML =
              `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-caret-up-fill" viewBox="0 0 16 16">
                <path d="m7.247 4.86-4.796 5.481c-.566.647-.106 1.659.753 1.659h9.592a1 1 0 0 0 .753-1.659l-4.796-5.48a1 1 0 0 0-1.506 0z"/>
              </svg>`
          }
          else {
            document.getElementById("th" + j).innerHTML = ''
          }
        }

        if (isiX > isiY) {
          shouldSwitch = true
          break
        }
      } else if (dir == "desc") {
        for (j = 0; j < colsLenMin1; j ++) {
          if (j === n) {
            document.getElementById("th" + j).innerHTML =
            `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-caret-down-fill" viewBox="0 0 16 16">
              <path d="M7.247 11.14 2.451 5.658C1.885 5.013 2.345 4 3.204 4h9.592a1 1 0 0 1 .753 1.659l-4.796 5.48a1 1 0 0 1-1.506 0z"/>
            </svg>`
          }
          else {
            document.getElementById("th" + j).innerHTML = ''
          }
        }

        if (isiX < isiY) {
          shouldSwitch = true
          break
        }
      }
    }

    if (shouldSwitch) {
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true
      switchcount++
    } else {
      if (switchcount == 0 && dir == "asc") {
        dir = "desc"
        switching = true
      }
    }
  }
}

/*
Search table

https://www.w3schools.com/howto/howto_js_filter_table.asp
*/
function searchTable() {
  let input, filter, table, tr, td, i, txtValue, j

  input = document.getElementById("searchTable")
  filter = input.value.toUpperCase()
  table = document.getElementById("table-item")
  tr = table.getElementsByTagName("tr")
  trLength = tr.length
  let colsLenMin1 = table.rows[0].cells.length - 1

  for (i = 0; i < trLength; i++) {
    for (j = 0; j < colsLenMin1; j++) {
      td = tr[i].getElementsByTagName("td")[j]
      if (td) {
        txtValue = td.textContent || td.innerText
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
          tr[i].style.display = ""
          i++
          j = 0
        } else {
          tr[i].style.display = "none"
        }
      }
    }
  }
}
