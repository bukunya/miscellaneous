import datetime
import os

class TodoSystem:
    def __init__(self):
        self.tasks = []
        self.task_id_counter = 1

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def add_task(self):
        print("\n=== TAMBAH TUGAS BARU ===")
        judul = input("Masukkan judul tugas: ").strip()
        if not judul:
            print("Judul tidak boleh kosong!")
            return

        deskripsi = input("Masukkan deskripsi tugas: ").strip()

        print("Pilih prioritas:")
        print("1. High")
        print("2. Medium")
        print("3. Low")
        prioritas_choice = input("Pilihan (1-3): ").strip()
        prioritas_map = {'1': 'High', '2': 'Medium', '3': 'Low'}
        prioritas = prioritas_map.get(prioritas_choice, 'Medium')

        deadline = input("Masukkan deadline (YYYY-MM-DD) atau enter untuk skip: ").strip()
        if deadline:
            try:
                datetime.datetime.strptime(deadline, '%Y-%m-%d')
            except ValueError:
                print("Format tanggal salah! Menggunakan tanggal hari ini.")
                deadline = datetime.date.today().strftime('%Y-%m-%d')
        else:
            deadline = "Tidak ada"

        new_task = {
            'id': self.task_id_counter,
            'judul': judul,
            'deskripsi': deskripsi,
            'prioritas': prioritas,
            'deadline': deadline,
            'status': 'Pending'
        }

        self.tasks.append(new_task)
        self.task_id_counter += 1

        print(f"✅ Tugas '{judul}' berhasil ditambahkan!")
        input("Tekan Enter untuk kembali...")

    def view_all_tasks(self):
        print("\n=== DAFTAR SEMUA TUGAS ===")
        if not self.tasks:
            print("Tidak ada tugas yang tersimpan.")
            input("Tekan Enter untuk kembali...")
            return

        print(f"{'ID':<3} {'Judul':<20} {'Status':<10} {'Deadline':<12}")
        print("-" * 50)

        for task in self.tasks:
            print(f"{task['id']:<3} {task['judul'][:18]:<20} {task['status']:<10} {task['deadline']:<12}")

        print(f"\nTotal tugas: {len(self.tasks)}")
        input("Tekan Enter untuk kembali...")

    def delete_task(self):
        print("\n=== HAPUS TUGAS ===")
        if not self.tasks:
            print("Tidak ada tugas untuk dihapus.")
            input("Tekan Enter untuk kembali...")
            return

        self.view_tasks_simple()
        try:
            task_id = int(input("Masukkan ID tugas yang akan dihapus: "))
            task_to_delete = None
            task_index = -1

            for i, task in enumerate(self.tasks):
                if task['id'] == task_id:
                    task_to_delete = task.copy()
                    task_index = i
                    break

            if task_to_delete:
                self.tasks.remove(self.tasks[task_index])
                print(f"✅ Tugas '{task_to_delete['judul']}' berhasil dihapus!")
            else:
                print("❌ ID tugas tidak ditemukan!")

        except ValueError:
            print("❌ ID harus berupa angka!")

        input("Tekan Enter untuk kembali...")

    def edit_task(self):
        print("\n=== EDIT TUGAS ===")
        if not self.tasks:
            print("Tidak ada tugas untuk diedit.")
            input("Tekan Enter untuk kembali...")
            return

        self.view_tasks_simple()
        try:
            task_id = int(input("Masukkan ID tugas yang akan diedit: "))
            task_to_edit = None

            for task in self.tasks:
                if task['id'] == task_id:
                    task_to_edit = task
                    break

            if not task_to_edit:
                print("❌ ID tugas tidak ditemukan!")
                input("Tekan Enter untuk kembali...")
                return

            print(f"\nMengedit tugas: {task_to_edit['judul']}")
            print("(Tekan Enter untuk tidak mengubah)")

            new_judul = input(f"Judul ({task_to_edit['judul']}): ").strip()
            if new_judul:
                task_to_edit['judul'] = new_judul

            new_deskripsi = input(f"Deskripsi ({task_to_edit['deskripsi']}): ").strip()
            if new_deskripsi:
                task_to_edit['deskripsi'] = new_deskripsi

            new_deadline = input(f"Deadline ({task_to_edit['deadline']}): ").strip()
            if new_deadline:
                try:
                    datetime.datetime.strptime(new_deadline, '%Y-%m-%d')
                    task_to_edit['deadline'] = new_deadline
                except ValueError:
                    print("Format tanggal salah! Deadline tidak diubah.")

            print("✅ Tugas berhasil diedit!")

        except ValueError:
            print("❌ ID harus berupa angka!")

        input("Tekan Enter untuk kembali...")

    def toggle_status(self):
        print("\n=== UBAH STATUS TUGAS ===")
        if not self.tasks:
            print("Tidak ada tugas.")
            input("Tekan Enter untuk kembali...")
            return

        self.view_tasks_simple()
        try:
            task_id = int(input("Masukkan ID tugas: "))
            task_to_toggle = None

            for task in self.tasks:
                if task['id'] == task_id:
                    task_to_toggle = task
                    break

            if task_to_toggle:
                new_status = 'Completed' if task_to_toggle['status'] == 'Pending' else 'Pending'
                task_to_toggle['status'] = new_status

                print(f"✅ Status tugas '{task_to_toggle['judul']}' diubah menjadi {new_status}!")
            else:
                print("❌ ID tugas tidak ditemukan!")

        except ValueError:
            print("❌ ID harus berupa angka!")

        input("Tekan Enter untuk kembali...")

    def search_tasks(self):
        print("\n=== CARI TUGAS ===")
        keyword = input("Masukkan kata kunci pencarian: ").strip().lower()

        if not keyword:
            print("Kata kunci tidak boleh kosong!")
            input("Tekan Enter untuk kembali...")
            return

        found_tasks = []
        for task in self.tasks:
            if keyword in task['judul'].lower() or keyword in task['deskripsi'].lower():
                found_tasks.append(task)

        if found_tasks:
            print(f"\n🔍 Ditemukan {len(found_tasks)} tugas:")
            print(f"{'ID':<3} {'Judul':<20} {'Prioritas':<8} {'Status':<10} {'Deadline':<12}")
            print("-" * 60)

            for task in found_tasks:
                print(f"{task['id']:<3} {task['judul'][:18]:<20} {task['prioritas']:<8} {task['status']:<10} {task['deadline']:<12}")
        else:
            print("❌ Tidak ada tugas yang ditemukan!")

        input("Tekan Enter untuk kembali...")

    def filter_by_status(self):
        print("\n=== FILTER BERDASARKAN STATUS ===")
        print("1. Pending")
        print("2. Completed")

        choice = input("Pilih status (1-2): ").strip()
        status_map = {'1': 'Pending', '2': 'Completed'}

        if choice not in status_map:
            print("❌ Pilihan tidak valid!")
            input("Tekan Enter untuk kembali...")
            return

        selected_status = status_map[choice]
        filtered_tasks = [task for task in self.tasks if task['status'] == selected_status]

        if filtered_tasks:
            print(f"\n📋 Tugas dengan status '{selected_status}' ({len(filtered_tasks)} tugas):")
            print(f"{'ID':<3} {'Judul':<20} {'Prioritas':<8} {'Deadline':<12}")
            print("-" * 50)

            for task in filtered_tasks:
                print(f"{task['id']:<3} {task['judul'][:18]:<20} {task['prioritas']:<8} {task['deadline']:<12}")
        else:
            print(f"❌ Tidak ada tugas dengan status '{selected_status}'!")

        input("Tekan Enter untuk kembali...")

    def filter_by_deadline(self):
        print("\n=== TUGAS BERDASARKAN DEADLINE ===")

        tasks_with_deadline = [task for task in self.tasks if task['deadline'] != "Tidak ada"]

        if not tasks_with_deadline:
            print("❌ Tidak ada tugas dengan deadline!")
            input("Tekan Enter untuk kembali...")
            return

        try:
            tasks_with_deadline.sort(key=lambda x: datetime.datetime.strptime(x['deadline'], '%Y-%m-%d'))
        except ValueError:
            print("❌ Ada error dalam format tanggal!")
            input("Tekan Enter untuk kembali...")
            return

        today = datetime.date.today()

        print(f"📅 Daftar tugas berdasarkan deadline ({len(tasks_with_deadline)} tugas):")
        print(f"{'ID':<3} {'Judul':<20} {'Status':<10} {'Deadline':<12} {'Urgency':<15}")
        print("-" * 65)

        for task in tasks_with_deadline:
            try:
                task_date = datetime.datetime.strptime(task['deadline'], '%Y-%m-%d').date()
                days_diff = (task_date - today).days

                if days_diff < 0:
                    urgency = "🔴 OVERDUE"
                elif days_diff == 0:
                    urgency = "🟠 HARI INI"
                elif days_diff == 1:
                    urgency = "🟡 BESOK"
                elif days_diff <= 7:
                    urgency = f"🟢 {days_diff} HARI"
                elif days_diff <= 30:
                    urgency = f"🔵 {days_diff} HARI"
                else:
                    urgency = f"⚪ {days_diff} HARI"

                print(f"{task['id']:<3} {task['judul'][:18]:<20} {task['status']:<10} {task['deadline']:<12} {urgency:<15}")

            except ValueError:
                print(f"{task['id']:<3} {task['judul'][:18]:<20} {task['status']:<10} {task['deadline']:<12} {'❌ FORMAT ERROR':<15}")

        overdue_count = sum(1 for task in tasks_with_deadline
                           if (datetime.datetime.strptime(task['deadline'], '%Y-%m-%d').date() - today).days < 0)
        today_count = sum(1 for task in tasks_with_deadline
                         if (datetime.datetime.strptime(task['deadline'], '%Y-%m-%d').date() - today).days == 0)

        print(f"\n📊 Summary:")
        print(f"   🔴 Overdue: {overdue_count} tugas")
        print(f"   🟠 Hari ini: {today_count} tugas")
        print(f"   📅 Total dengan deadline: {len(tasks_with_deadline)} tugas")

        input("Tekan Enter untuk kembali...")

    def view_tasks_simple(self):
        if not self.tasks:
            print("Tidak ada tugas.")
            return

        print(f"{'ID':<3} {'Judul':<25} {'Status':<10}")
        print("-" * 40)
        for task in self.tasks:
            print(f"{task['id']:<3} {task['judul'][:23]:<25} {task['status']:<10}")
        print()

    def show_menu(self):
        print("\n" + "="*50)
        print("🗂️  SISTEM MANAJEMEN TUGAS (TO-DO LIST)")
        print("="*50)
        print("1.  📝 Tambah Tugas Baru")
        print("2.  📋 Lihat Semua Tugas")
        print("3.  🗑️  Hapus Tugas")
        print("4.  ✏️  Edit Tugas")
        print("5.  ✅ Ubah Status Tugas")
        print("6.  🔍 Cari Tugas")
        print("7.  📊 Filter berdasarkan Status")
        print("8.  📅 Filter berdasarkan Deadline")
        print("0.  🚪 Keluar")
        print("="*50)

    def run(self):
        while True:
            self.clear_screen()
            self.show_menu()

            choice = input("Pilih menu (0-8): ").strip()

            if choice == '1':  
                self.add_task()
            elif choice == '2':
                self.view_all_tasks()
            elif choice == '3':
                self.delete_task()
            elif choice == '4':
                self.edit_task()
            elif choice == '5':
                self.toggle_status()
            elif choice == '6':
                self.search_tasks()
            elif choice == '7':
                self.filter_by_status()
            elif choice == '8':
                self.filter_by_deadline()
            elif choice == '0':
                print("\n👋 Terima kasih telah menggunakan Sistem Manajemen Tugas!")
                print("Sampai jumpa!")
                break
            else:
                print("❌ Pilihan tidak valid! Silakan pilih 0-8.")
                input("Tekan Enter untuk melanjutkan...")

if __name__ == "__main__":
    print("🚀 Memulai Sistem Manajemen Tugas...")
    todo_system = TodoSystem()
    todo_system.run()