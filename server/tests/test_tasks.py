from tests.base.test_base import TestViewSetBase
from todo.models import Task


class TestTaskViewSet(TestViewSetBase):
    base_name = "tasks"
    pagination = True

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.task1 = Task.objects.create(
            title="Task One", description="Description 1", completed=True
        )
        cls.task2 = Task.objects.create(
            title="Task Two", description="Description 2", completed=False
        )

    def test_list_tasks(self) -> None:
        response = self.list()

        assert response == [
            self.get_expected_task_detail(self.task1),
            self.get_expected_task_detail(self.task2),
        ]

    def test_retrieve_task(self) -> None:
        response = self.retrieve({"id": self.task1.id})

        assert response == self.get_expected_task_detail(self.task1)

    def test_update_task(self) -> None:
        updated_attrs = {
            "title": "Updated title 1",
            "description": "Updated description1",
            "completed": False,
        }
        response = self.update({"id": self.task1.id}, updated_attrs)

        assert response == {
            **self.get_expected_task_detail(self.task1),
            **updated_attrs,
        }

    def test_partial_update_task(self) -> None:
        updated_attrs = {
            "title": "Partial Updated title 1",
        }
        response = self.partial_update({"id": self.task1.id}, updated_attrs)

        assert response == {
            **self.get_expected_task_detail(self.task1),
            **updated_attrs,
        }

    def test_delete_task(self) -> None:
        self.delete({"id": self.task1.id})

        assert self.list() == [self.get_expected_task_detail(self.task2)]

    def get_expected_task_detail(self, task: Task) -> dict:
        return {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "updated_at": task.updated_at.strftime("%Y-%m-%d %H:%M")
        }
