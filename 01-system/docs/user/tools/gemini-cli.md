# Gemini CLI ���X�ЫԲu
**e**��llms  
**�汾**��v0.1 (�������ڣ�2025-11-17)

## �������[
- �ϥ� Google Gemini CLI ���b�u�ඣĪ����枵ك��P���޳N�Ұʪ��ܤu
- ���Y�������W���ɭԡB���y POC ���\��w�u���y
- �R�O�����e�����`03-outputs/gemini-cli/` ���ΨӶ}�����귽

## �����f��
- `Targets`�������U����ܤ覡�����ݩʳ����ɮצ���t
- `Query`�������ܤ覡���᪺���q�ثe���j
- `Model`�����q�Τ֡A�����K�ϥδ]�w�߻P��������
- `OutputName`������X�̾ڨ�W�١A�ɭԤ��w��Ʈw�@���Ѥp���}�l

## ��Ҋ�÷����𲽣�
1. �T�w�����Ū��a�� (���� repo root) �öi�� `@` ����d
2. ���ɮ׼Ʊ`pwsh tools/gemini-run.ps1 -Targets @('src/', 'tests/') -Query '���ݨ䪺���P�ؿ�'`
3. ���� CLI ���ͪ����G�ñN prompt/response ��W���`03-outputs/gemini-cli/<���>` ��

## ����
- **���ٹ���**��`03-outputs/gemini-cli/<run-id>/prompt.txt` ���P `response.txt`
- **�M�A����**��`03-outputs/gemini-cli/<run-id>/`

## ݔ�� / ݔ��·��
- ݔ���Դ��`02-inputs/...`
- �a��λ�ã�`03-outputs/gemini-cli/`

## �L�U�c����
- Gemini CLI �� API Key �]�­��b�W���Ѿl�檺���W�Y�����ƾ�O
- ���ɮ׼ƱN `@` ��ܽd���|��b���O�W�L 100KB ���g�u���

## �����ų�
- ��Ҋ�e�`�c�ⷨ���B�Y `01-system/docs/agents/TROUBLESHOOTING.md` ���P�lĿ����

## �汾�c���¼o�
- v0.1��2025-11-17�������档
