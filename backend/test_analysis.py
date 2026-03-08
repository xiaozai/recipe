import asyncio
import sys
sys.path.insert(0, '.')

from app.models.content import ContentItem, ContentType
from app.ai import TrendAnalyzer

async def test():
    item = ContentItem(
        id='test_1',
        title='Test Project',
        content='This is a test project for Python programming',
        source_type=ContentType.GITHUB_REPO,
        url='https://test.com',
    )
    analyzer = TrendAnalyzer()
    print("Starting analysis...")
    try:
        result = await analyzer.analyze_single_project(item, 'test')
        print('Result:', result)
    except Exception as e:
        print(f'Error: {e}')
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    asyncio.run(test())
