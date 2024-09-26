library(shiny)
library(ggplot2)

# Функция для сортировки пузырьком
bubble_sort <- function(x) {
  n <- length(x)
  for (i in 1:(n-1)) {
    for (j in 1:(n-i)) {
      if (x[j] > x[j+1]) {
        temp <- x[j]
        x[j] <- x[j+1]
        x[j+1] <- temp
      }
    }
  }
  return(x)
}

# Функция для бинарного поиска
binary_search <- function(x, target) {
  left <- 1
  right <- length(x)
  while (left <= right) {
    mid <- floor((left + right) / 2)
    if (x[mid] == target) {
      return(mid)
    } else if (x[mid] < target) {
      left <- mid + 1
    } else {
      right <- mid - 1
    }
  }
  return(-1)
}

# UI Shiny-приложения
ui <- fluidPage(
  titlePanel("Сортировка: Пузырьковая vs Бинарный поиск"),
  sidebarLayout(
    sidebarPanel(
      sliderInput("n", "Количество элементов:", min = 100, max = 5000, value = 1000, step = 100),
      actionButton("run", "Запустить")
    ),
    mainPanel(
      plotOutput("plot"),
      verbatimTextOutput("results"),
      uiOutput("progress")
    )
  )
)

# Сервер Shiny-приложения
server <- function(input, output) {
  # Реактивный объект для хранения времени выполнения
  times <- reactiveValues(bubble = NULL, binary = NULL)

  # Функция для запуска сортировки
  observeEvent(input$run, {
    # Получение значения слайдера
    n <- input$n

    # Создание прогресс бара
    withProgress(message = "Выполняется сортировка...", value = 0, {
      # Создание случайного массива
      x <- sample(1:n, n)

      # Измерение времени выполнения сортировки пузырьком
      start_time <- Sys.time()
      bubble_sort(x)
      end_time <- Sys.time()
      times$bubble <- end_time - start_time

      # Измерение времени выполнения бинарного поиска
      start_time <- Sys.time()
      binary_search(sort(x), x[1])
      end_time <- Sys.time()
      times$binary <- end_time - start_time

      # Обновление прогресс бара
      incProgress(1, detail = "Сортировка завершена")
    })
  })

  # Вывод результатов
  output$results <- renderPrint({
    if (!is.null(times$bubble) && !is.null(times$binary)) {
      cat("Время сортировки пузырьком:", times$bubble, "\n")
      cat("Время сортировки бинарным поиском:", times$binary, "\n")
    }
  })

  # Вывод графика
  output$plot <- renderPlot({
    if (!is.null(times$bubble) && !is.null(times$binary)) {
      ggplot(data.frame(Algorithm = c("Bubble Sort", "Binary Search"), Time = c(times$bubble, times$binary)), aes(x = Algorithm, y = Time, fill = Algorithm)) +
        geom_bar(stat = "identity") +
        labs(title = "Сравнение времени выполнения", x = "Алгоритм", y = "Время (сек)") +
        scale_fill_manual(values = c("Bubble Sort" = "blue", "Binary Search" = "red"))
    }
  })


  # Вывод прогресс бара
  output$progress <- renderUI({
    if (!is.null(times$bubble) && !is.null(times$binary)) {
      NULL
    } else {
      progressBar("progress", "Выполняется сортировка...", value = 0)
    }
  })
}

# Запуск приложения Shiny
shinyApp(ui = ui, server = server)