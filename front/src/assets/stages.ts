const stage1 = [
  {
    title: 'План строительства',
    stages: [
      {
        title: 'Утверждение плана строительства',
        flags: {
          isPlanning: true,
        },
        attributes: [
          {
            name: 'Номер проекта',
            code: 'project_number',
            type: 'text',
          },
          {
            name: 'Дата утверждения',
            code: 'approval_date',
            type: 'text',
          },
          {
            name: 'Ответственный',
            code: 'responsible_person',
            type: 'text',
          },
          {
            name: 'Документ плана',
            code: 'plan_document',
            type: 'attachment',
          },
        ],
      },
    ],
  },
  {
    title: 'Госзакупки',
    stages: [
      {
        title: 'Публикация тендера',
        flags: {
          isPlanning: false,
        },
        attributes: [
          {
            name: 'Номер тендера',
            code: 'tender_number',
            type: 'text',
          },
        ],
      },
      {
        title: 'Выбор подрядчика',
        flags: {
          isPlanning: false,
        },
        attributes: [
          {
            name: 'Название подрядчика',
            code: 'contractor_name',
            type: 'text',
          },
        ],
      },
      {
        title: 'Контракт',
        flags: {
          isPlanning: false,
        },
        attributes: [
          {
            name: 'Номер контракта',
            code: 'contract_number',
            type: 'text',
          },
        ],
      },
    ],
  },
  {
    title: 'Проектирование',
    stages: [
      {
        title: 'Проектирование',
        flags: {
          isPlanning: false,
        },
        attributes: [
          {
            name: 'Главный инженер проекта',
            code: 'chief_engineer',
            type: 'text',
          },
        ],
      },
      {
        title: 'Геологические изыскания',
        flags: {
          isPlanning: false,
        },
        attributes: [
          {
            name: 'Отчет по изысканиям',
            code: 'survey_report',
            type: 'attachment',
          },
        ],
      },
    ],
  },
  {
    title: 'Строительство',
    stages: [
      {
        title: 'Расчистка территории',
        flags: {
          isPlanning: false,
        },
        attributes: [
          {
            name: 'Подрядчик по расчистке',
            code: 'clearing_contractor',
            type: 'text',
          },
        ],
      },
      {
        title: 'Земляные работы',
        flags: {
          isPlanning: false,
        },
        attributes: [
          {
            name: 'Объем земляных работ',
            code: 'earthwork_volume',
            type: 'text',
          },
        ],
      },
      {
        title: 'Работа с коммуникациями',
        flags: {
          isPlanning: false,
        },
        attributes: [
          {
            name: 'Схема коммуникаций',
            code: 'utility_layout',
            type: 'attachment',
          },
        ],
      },
      {
        title: 'Подстилающий слой',
        flags: {
          isPlanning: false,
        },
        attributes: [
          {
            name: 'Материал подстилающего слоя',
            code: 'subbase_material',
            type: 'text',
          },
        ],
      },
      {
        title: 'Асфальтовое покрытие',
        flags: {
          isPlanning: false,
        },
        attributes: [
          {
            name: 'Тип асфальтобетона',
            code: 'asphalt_type',
            type: 'text',
          },
        ],
      },
      {
        title: 'Нанесение разметки и благоустройство',
        flags: {
          isPlanning: false,
        },
        attributes: [
          {
            name: 'План благоустройства',
            code: 'landscaping_plan',
            type: 'attachment',
          },
        ],
      },
      {
        title: 'Шумоизоляция',
        flags: {
          isPlanning: false,
        },
        attributes: [
          {
            name: 'Материал шумоизоляции',
            code: 'noise_insulation_material',
            type: 'text',
          },
        ],
      },
    ],
  },
];
export { stage1 };
