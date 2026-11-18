
from Lab4_Semenova_validators import input_mass, input_humidity1, input_humidity2, input_temp
from Lab4_Semenova_menu import show_menu, select_mode, mode_name
from Lab4_Semenova_operations import mass_removed, drying_time, tau_class


def main() -> None:
    """Главный сценарий."""
    print("=== Расчёт времени сушки влажного материала ===")

    while True:
        show_menu()
        k = select_mode()
        if k is None:
            print("Работа завершена.")
            break

        m = input_mass()
        w1 = input_humidity1()
        w2 = input_humidity2()
        t = input_temp()

        m_w = mass_removed(m, w1, w2)
        tau = drying_time(k, w1, w2)
        cls = tau_class(tau)

        print("\n Результаты ")
        print(f"Режим:        {mode_name(k)} (k = {k})")
        print(f"m_w (масса удаляемой воды):      {m_w:.2f} кг")
        print(f"Время сушки tau: {tau:.2f}, час")
        print(f"Класс: {cls}")
        print("\n")


if __name__ == "__main__":
    main()